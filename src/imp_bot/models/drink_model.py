from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator, root_validator

class DrinkModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True,
        validate_by_alias=True,
    )
    drink_id: str = Field(..., alias='idDrink')
    name: str = Field(..., alias='strDrink')
    alternative: Optional[str] = Field(default=None, alias='strDrinkAlternate')
    tags: Optional[str] = Field(default=None, alias='strTags')
    video: Optional[str] = Field(default=None, alias='strVideo')
    category: str = Field(..., alias='strCategory')
    iba: Optional[str] = Field(default=None, alias='strIBA')
    is_alcoholic: str = Field(default=False)
    glass: str = Field(..., alias='strGlass')
    instructions: str = Field(..., alias='strInstructions')
    drink_thumb: Optional[str] = Field(default=None, alias='strDrinkThumb')
    ingredient_measurements: list[str] = Field(default_factory=list)
    imageSource: Optional[str] = Field(default=None, alias='strImageSource')
    imageAttribution: Optional[str] = Field(default=None, alias='strImageAttribution')
    creativeCommonsConfirmed: Optional[str] = Field(default=None, alias='strCreativeCommonsConfirmed')
    dateModified: Optional[str] = Field(default=None, alias='dateModified')
    
    @classmethod
    def model_validate(cls, obj: Any, **kwargs) -> "DrinkModel":
        """Custom validate method to process ingredients and alcoholic status before creating model"""
        if isinstance(obj, dict):
            # Process ingredients and measurements
            ingredients_list = []
            for i in range(1, 16):
                ingredient = obj.get(f'strIngredient{i}')
                measure = obj.get(f'strMeasure{i}')
                
                if ingredient and ingredient.strip():  # Check if ingredient exists and is not just whitespace
                    # If measure exists, combine them, otherwise just use ingredient
                    if measure and measure.strip():
                        ingredients_list.append(f"{measure.strip()} {ingredient.strip()}")
                    else:
                        ingredients_list.append(ingredient.strip())
            
            # Add processed ingredients to the object
            obj['ingredient_measurements'] = ingredients_list
            
            # Process alcoholic status
            obj['is_alcoholic'] = "Yes" if obj.get('strAlcoholic') == 'Alcoholic' else "No"
            
            # We can now remove the individual ingredient and measure fields
            # This is optional, as our model already ignores extra fields
            
        return super().model_validate(obj, **kwargs)


    def to_dict(self):
        return self.model_dump(exclude_defaults=True, exclude_none=True)

    def to_json(self):
        return self.model_dump_json(exclude_defaults=True, exclude_none=True)