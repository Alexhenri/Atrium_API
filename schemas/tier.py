from pydantic import BaseModel
from typing import List
from model.tier import Tier

class TierSchema(BaseModel):
    # Defines how a tier object need to be when inserted in db
    name: str = "Standard"
    cost_value: float = 84.99
    selling_price: float = 109.99


class SearchTierByNameSchema(BaseModel):
    # Defines how you will find any tier with their name
    name: str = "Standard"
    

def show_tiers(tiers: List[Tier]):
    # Return the tiers as defined in  TierViewSchema.
    result = []
    for tier in tiers:
        result.append({
            "id": tier.id,
            "name": tier.name,
            "cost_value":tier.cost_value,
            "selling_price":tier.selling_price
        })

    return {"tiers": result}


class TierViewSchema(BaseModel):
    # Defines the tier view, that is how the tier is returned
    id: int = 1
    name: str = "Nix"
    cost_value: float = 84.99
    selling_price: float = 109.00


class ListTierSchema(BaseModel):
    # Defines how to return the tier list
    tiers:List[TierViewSchema]


def show_tier(tier: Tier):
    # Return the tier as defined in TierViewSchema
    return {
        "id": tier.id,
        "name": tier.name,
        "cost_value": tier.cost_value,
        "selling_price": tier.selling_price
    }
