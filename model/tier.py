from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from  model import Base


class Tier(Base):
    __tablename__ = 'tier'

    id = Column("pk_tier", Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    cost_value = Column(Float)
    selling_price = Column(Float)

    # relationshop between glasses and tier 
    glasses = relationship('Glasses', back_populates='tier_rel')

    def __init__(self, name:str, cost_value:float, selling_price:float):
        """
        Create a tier object in the database

        Arguments:
            name: the tier name
            cost_value: how much a unity of this tier costs
            selling_price: recommend selling price of a glasses unity of this tier 
        """
        self.name = name
        self.cost_value = cost_value
        self.selling_price = selling_price