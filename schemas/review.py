from pydantic import BaseModel, validator


class ReviewSchema(BaseModel):
    # Defines how a new review should be
    glasses_id: int = 1
    text: str = "Just buy it, its a beautiful glasses!"
    stars: int = 5
    
    # Schema helping to enforce constraint integrity
    @validator('stars')
    def validate_stars_range(cls, value):
        if value < 1 or value > 5:
            raise ValueError("Stars must be between 1 and 5")
        return value
