from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator, root_validator

class DrinkListItemModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True,
        validate_by_alias=True,
    )
    drink_id: str = Field(..., alias='idDrink')


class DrinkListModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True,
        validate_by_alias=True,
    )

    drinks: list[DrinkListItemModel] = Field(default_factory=list)

    def to_dict(self):
        return self.model_dump(exclude_defaults=True, exclude_none=True)

    def to_json(self):
        return self.model_dump_json(exclude_defaults=True, exclude_none=True)