from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from datetime import datetime
from typing import Union

from  model import Base


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    text = Column(String(4000))
    stars = Column(Integer)
    
    entry_date = Column(DateTime, default=datetime.now())

    glasses = Column(Integer, ForeignKey("glasses.pk_glasses"), nullable=False)

    # Define a CheckConstraint to ensure stars are between 1 and 5
    __table_args__ = ( 
        # Defined like that because __table_args__ value must be a tuple, dict, or None
        CheckConstraint('stars >= 1 AND stars <= 5', name='check_stars_range'),
    )

    def __init__(self, text:str, stars: int, entry_date:Union[DateTime, None] = None):
        """
        Creates a review object in database

        Arguments:
            text: the review text
            entry_date: column to represent the entry date of the review in database 
        """
        self.text = text
        self.stars = stars
        if entry_date:
            self.entry_date = entry_date
