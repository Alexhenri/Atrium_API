from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import event
import os

# importing all tables defined 
from model.base import Base
from model.review import Review
from model.tier import Tier
from model.glasses import Glasses


db_path = "database/"
# Check if database dir already exist 
if not os.path.exists(db_path):
   # if not, create it 
   os.makedirs(db_path)

# url to access the sqlite database, local access
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# create the conection with database
engine = create_engine(db_url, echo=False)

# enable foreign keys constraints
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

event.listen(engine, 'connect', _fk_pragma_on_connect)

# create a session
Session = sessionmaker(bind=engine)

# create the db if it do not exist
if not database_exists(engine.url):
    create_database(engine.url) 

# create all tables in db, if they  do not exist
Base.metadata.create_all(engine)
