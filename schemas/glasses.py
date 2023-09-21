from pydantic import BaseModel
from typing import Optional, List, Dict
from model.glasses import Glasses

from schemas import ReviewSchema

class GlassesSchema(BaseModel):
    # Defines how a glasses object need to be when inserted in db
    name: str = "Nix"
    gender_target: str = "M"
    tier: int = 1
    is_sunglasses: bool = True
    frame_material: str = "Acetato"
    color: str = "Blue"
    image: Optional[str] = "nix_blue_image.png"
    quantity: int = 10
    descr: Optional[str] = "It has a retro design, with a 100% acetate frame that complements any style."


class SearchGlassesByNameSchema(BaseModel):
    # Defines how you will find any glasses with their name
    name: str = "Nix"


class SearchGlassesByMaterialSchema(BaseModel):
    # Defines how you will find any glasses with a specifc material
    frame_material: str = "Acetato"


class SearchGlassesByColorSchema(BaseModel):
    # Defines how you will find any glasses with a specifc color
    color: str = "Blue"


class SearchGlassesByGenderTargetSchema(BaseModel):
    # Defines how you will find any glasses with a specifc gender target
    gender_target: str = "M"


class SearchGlassesBySunglassesFilterSchema(BaseModel):
    # Defines how you will find any glasses that is or not a sunglasses
    is_sunglasses: str = True
    

class ListGlassesSchema(BaseModel):
    # Defines how to return the glasses list
    glasses:List[GlassesSchema]


def show_all_glasses(all_glasses: List[Glasses]):
    # Return all the glasses as defined in GlassesViewSchema
    result = []
    
    # matching_tier: Tier
    # for tier in glasses.tier_rel:
    #     print("DEBUG")
    #     if tier.id == all_glasses.id:
    #         matching_tier = tier
    #         break

    for glasses in all_glasses:
        print(glasses.tier_rel.name)
        result.append({
            "name": glasses.name,
            # Object of type Boolean is not JSON serializable
            "is_sunglasses": str(glasses.is_sunglasses),
            "frame_material": glasses.frame_material,
            "gender_target": glasses.gender_target,
            "tier": {"name": glasses.tier_rel.name, "selling_price": glasses.tier_rel.selling_price},
            "descr": glasses.descr,
            "image": glasses.image
        })

    return {"glasses": result}


class GlassesViewSchema(BaseModel):
    """"
    Defines how glasses will return:
        glasses + tier + comment 
    Obs: we have some images in database, but you can input some https://urltoyourimage.com
    """
    id: int = 1
    nome: str = "Nix"
    descr:str = "It has a retro design, with a 100% acetate frame that complements any style."
    gender_target: str = "M"
    is_sunglasses = False
    frame_material: str = "Acetato"
    color: str = "Blue"
    image: Optional[str] = "nix_blue_image.png"
    quantity: int = 10
    tier: Dict[str, float] = {"name": "Standard", "selling_price": 109.99}
    reviews:List[ReviewSchema] 
    total_reviews: int = 1


class GlassesDelSchema(BaseModel):
    # Defines what returns after a deletion request
    mesage: str
    nome: str


def show_glasses(glasses: Glasses):
    # Return the glasses as defined in GlassesViewSchema
    return {
        "id": glasses.id,
        "name": glasses.name,
        "descr": glasses.descr,
        "gender_target": glasses.gender_target,
        # Object of type Boolean is not JSON serializable
        "is_sunglasses": str(glasses.is_sunglasses),
        "frame_material": glasses.frame_material,
        "tier": {"name": glasses.tier_rel.name, "selling_price": glasses.tier_rel.selling_price},
        "quantity": glasses.quantity,
        "color": glasses.color,
        "image": glasses.image,
        "total_reviews": len(glasses.reviews),
        "reviews": [{"text": c.text, "stars": c.stars} for c in glasses.reviews]
    }
