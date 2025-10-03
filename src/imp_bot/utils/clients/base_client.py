from httpx import AsyncClient, HTTPError, TimeoutException, RequestError
import logging
from typing import Optional, Dict, Any, ClassVar, Type, TypeVar
import asyncio
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ClientError(Exception):
    """Base exception for client errors."""
    pass

T = TypeVar('T', bound='BaseHttpClient')

class BaseHttpClient(ABC):
    """Abstract base class for HTTP clients."""
    
    _client: ClassVar[Optional[AsyncClient]] = None
    DEFAULT_TIMEOUT: ClassVar[float] = 10.0
    MAX_RETRIES: ClassVar[int] = 2
    RETRY_DELAY: ClassVar[float] = 1.0  # seconds
    
    @classmethod
    async def get_client(cls: Type[T]) -> AsyncClient:
        """Get or create the shared client instance."""
        if cls._client is None or cls._client.is_closed:
            cls._client = AsyncClient(
                timeout=cls.DEFAULT_TIMEOUT,
                follow_redirects=True
            )
        return cls._client
    
    @classmethod
    async def close_client(cls: Type[T]) -> None:
        """Close the client connection if it exists."""
        if cls._client is not None and not cls._client.is_closed:
            await cls._client.aclose()
            cls._client = None
    
    @classmethod
    async def _make_request(
        cls: Type[T], 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        retries: int = None
    ) -> dict:
        """Make an HTTP request with retries and error handling."""
        if retries is None:
            retries = cls.MAX_RETRIES
            
        attempt = 0
        last_error = None
        
        while attempt <= retries:
            try:
                client = await cls.get_client()
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    logger.warning(f"Empty response from {url}")
                    return {"error": "API returned empty response"}
                return data
                
            except (HTTPError, RequestError) as e:
                logger.warning(f"Attempt {attempt+1}/{retries+1} failed: {e}")
                last_error = e
                
                # Don't retry on 4xx client errors except 429 (rate limiting)
                if isinstance(e, HTTPError) and 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                    break
                
                # Wait before retrying
                if attempt < retries:
                    await asyncio.sleep(cls.RETRY_DELAY * (attempt + 1))
                
            except Exception as e:
                logger.error(f"Unexpected error accessing {url}: {e}")
                last_error = e
                break
                
            attempt += 1
        
        # If we got here, all attempts failed
        error_message = str(last_error) if last_error else "Unknown error"
        logger.error(f"All {retries+1} attempts failed for {url}: {error_message}")
        return {"error": f"API request failed: {error_message}"}
    
    @classmethod
    @abstractmethod
    def _safe_url(cls, base_url: str, param: str) -> str:
        """Create a safe URL with proper encoding of parameters.
        
        This method must be implemented by subclasses.
        """
        pass
    
    @classmethod
    @abstractmethod
    def _validate_response(cls, data: dict) -> dict:
        """Validate the API response data structure.
        
        This method must be implemented by subclasses.
        """
        pass