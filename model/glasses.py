from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import  Base, Review, Tier
            

class Glasses(Base):
    __tablename__ = 'glasses'

    id = Column("pk_glasses", Integer, primary_key=True)
    name = Column(String(140), unique=True, nullable=False)
    descr = Column(String(512))
    tier = Column("fk_tier", Integer, ForeignKey("tier.pk_tier"), nullable=False)
    date_createad = Column(DateTime, default=datetime.now(), nullable=False)
    gender_target = Column(String(10))
    is_sunglasses = Column(Boolean)
    frame_material = Column(String(50), nullable=False)
    color = Column(String(50))
    image = Column(String(255))
    quantity = Column(Integer)
    
    #This relationships, SQLAlchemy will be responsable to create

    tier_rel = relationship("Tier", back_populates='glasses')
    """
        Reviews that anyone can post about the glasses
        It's different from description, that is the producer comment about the glasses
    """
    reviews = relationship("Review")

     # Define a ForeignKeyConstraint to enforce the foreign key relationship
    ForeignKeyConstraint(
        ['fk_tier'],
        ['tier.pk_tier'],
        name='fk_tier_glasses'
    )

    def __init__(self, name:str, descr:str, tier:int,  
                 gender_target:str, is_sunglasses:bool, frame_material:str,
                 color:str, image:str, quantity: int,
                 date_created:Union[DateTime, None] = None):
        """
        Create a Glasses 

        Arguments:
            name: glasses name/model
            descr: description of the glasses
            tier: specify a tier id from tier table as foreign key
            date_created: insertion date in database
            gender_target: specifies if the glasses is indicated for M, F or U. Male, female and unisex, respectively
            is_sunglasses: True if sunglasses
            frame_material: specifies the frame material. ex: wood, iron, plastic... 
            color: specifies the predominant color 
            image: image path of a specific pair of glasses
            quantity: quantity of a specific pair of glasses
        """

        self.name = name
        self.descr = descr
        self.tier = tier
        self.date_created = date_created
        self.gender_target = gender_target
        self.is_sunglasses = is_sunglasses
        self.frame_material = frame_material
        self.color = color
        self.image = image
        self.quantity = quantity


    def add_review(self, review:Review):
        #Add a new review to Glasses 
        self.reviews.append(review)


    def add_tier(self, tier:Tier):
        #Add a new tier to Glasses 
        self.tier_rel.append(tier)

