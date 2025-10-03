import logging
import random
from enum import Enum
from urllib.parse import quote
from imp_bot.models.drink_list_model import DrinkListModel
from imp_bot.utils.clients.base_client import BaseHttpClient, ClientError


logger = logging.getLogger(__name__)

class HttpxClientEndpoints(Enum):
    BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1"
    RANDOM_DRINK_URL = f"{BASE_URL}/random.php"
    INGREDIENT_FILTER_URL = f"{BASE_URL}/filter.php?i="
    ALCOHOLIC_DRINKS_URL = f"{BASE_URL}/filter.php?a=Alcoholic"
    NON_ALCOHOLIC_DRINKS_URL = f"{BASE_URL}/filter.php?a=Non_Alcoholic"
    SEARCH_BY_NAME_URL = f"{BASE_URL}/search.php?s="
    SEARCH_BY_ID = f"{BASE_URL}/lookup.php?i="


class BartenderClientError(ClientError):
    """Specific exception for BartenderClient errors."""
    pass
    
class BartenderClient(BaseHttpClient):
    """Client for interacting with the CocktailDB API."""
    
    @classmethod
    def _safe_url(cls, base_url: str, param: str) -> str:
        """Create a safe URL with proper encoding of parameters."""
        return f"{base_url}{quote(param.strip())}"
    
    @classmethod
    def _validate_response(cls, data: dict) -> dict:
        """Validate the API response data structure."""
        if "error" in data:
            return data
        if "drinks" not in data:
            return {"error": "Invalid API response format: missing 'drinks' key"}
        if data["drinks"] is None:
            return {"drinks": []}
        return data
    
    @classmethod
    async def get_random_drink_json(cls) -> dict:
        """Get a random drink from the API."""
        data = await cls._make_request(HttpxClientEndpoints.RANDOM_DRINK_URL.value)
        return cls._validate_response(data)
        

    
    @classmethod
    async def search_drinks_by_name(cls, name: str) -> dict:
        """Search for drinks by name."""
        if not name or not name.strip():
            return {"error": "Name parameter cannot be empty"}
            
        url = cls._safe_url(HttpxClientEndpoints.SEARCH_BY_NAME_URL.value, name)
        data = await cls._make_request(url)
        return cls._validate_response(data)
    
    @classmethod
    async def _search_drink_by_id(cls, drink_id: str) -> dict:
        """Get a drink by its ID."""
        if not drink_id or not drink_id.strip():
            return {"error": "Drink ID parameter cannot be empty"}

        url = cls._safe_url(HttpxClientEndpoints.SEARCH_BY_ID.value, drink_id)
        data = await cls._make_request(url)
        return cls._validate_response(data)
    
    @classmethod
    async def _handle_drink_list_data(cls, data: dict) -> dict:
        """Get a drink by its ID."""
        drink_list_json = cls._validate_response(data)
        drink_list_model = DrinkListModel.model_validate(drink_list_json)
        
        random_drink_item = random.choice(drink_list_model.drinks)
        
        drink_id = random_drink_item.drink_id
        data = await cls._search_drink_by_id(drink_id)
        return cls._validate_response(data)
    
    @classmethod
    async def get_drink_list_by_ingredient(cls, ingredient: str) -> dict:
        """Get drinks filtered by ingredient."""
        if not ingredient or not ingredient.strip():
            return {"error": "Ingredient parameter cannot be empty"}
            
        url = cls._safe_url(HttpxClientEndpoints.INGREDIENT_FILTER_URL.value, ingredient)
        data = await cls._make_request(url)
        return await cls._handle_drink_list_data(data)
        
    @classmethod
    async def get_alcoholic_drinks(cls) -> dict:
        """Get a list of alcoholic drinks."""
        data = await cls._make_request(HttpxClientEndpoints.ALCOHOLIC_DRINKS_URL.value)
        return await cls._handle_drink_list_data(data)

        
    @classmethod
    async def get_non_alcoholic_drinks(cls) -> dict:
        """Get a list of non-alcoholic drinks."""
        data = await cls._make_request(HttpxClientEndpoints.NON_ALCOHOLIC_DRINKS_URL.value)
        return await cls._handle_drink_list_data(data)
