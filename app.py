from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Glasses, Review, Tier
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Atrium API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentation", description="Documentation selection: Swagger, Redoc, or RapiDoc")
glasses_tag = Tag(name="Glasses", description="Addition, viewing and deletion of glasses in the database")
tier_tag = Tag(name="Tier", description="Addition, viewing and deletion of tier in the database")
review_tag = Tag(name="Review", description="Add a review to a registered glasses in the database")


@app.get('/', tags=[home_tag])
def home():
    """
    Redirects to /openapi, a screen that allows the choice of documentation style
    """
    return redirect('/openapi')

@app.post('/tier', tags=[tier_tag],
          responses={"200":TierViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tier(form: TierSchema):
    """
      Adds a new Tier to the database
      Returns a representation view of the tiers
    """
    tier = Tier(
        name= form.name,
        cost_value= form.cost_value,
        selling_price= form.selling_price
        )
    logger.debug(f"Adding tier: '{tier.name}'")
    try:
        # Creating a connection to the database
        session = Session()
        # Adding tier
        session.add(tier)
        # Executing the command to add a new tier to the table
        session.commit()
        logger.debug(f"Added tier: '{tier.name}' in the database")
        return show_tier(tier), 200

    except IntegrityError as e:
        # Assuming that the problem of name duplication is the likely reason
        error_msg = "Sorry but we already have a tier with the same name in the database"
        logger.warning(f"Error while trying tod add: '{tier.name}', {error_msg}")
        return {"msg": error_msg}, 409

    except Exception as e:
        # In case of an unexpected error
        error_msg = "Sorry but was not possible to add the new tier"
        logger.warning(f"Unexpected while trying to add tier: '{tier.name}', {error_msg}")
        return {"msg": error_msg}, 400
    
@app.get('/tiers', tags=[tier_tag],
         responses={"200": ListTierSchema, "404": ErrorSchema})
def get_tiers():
    """
        Performs a search for all registered tiers
        Returns a representation view of the tiers list
    """
    logger.debug(f"Collecting tiers")
    # Creating a connection to the database
    session = Session()
    # Performing the search
    tiers = session.query(Tier).all()

    if not tiers:
        # If there are no tiers registered in the database
        return {"tiers": []}, 200
    else:
        logger.debug(f"%d tiers found" % len(tiers))
        # Returns the representation view of the tier list
        return show_tiers(tiers), 200


@app.post('/glasses', tags=[glasses_tag],
          responses={"200": GlassesViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_glasses(form: GlassesSchema):
    """
        Adds a new Glasses to the database
        Returns a representation view of the glasses
    """
    glasses = Glasses(
        name= form.name,
        descr= form.descr,
        tier= form.tier,
        gender_target= form.gender_target,
        is_sunglasses= form.is_sunglasses,
        frame_material= form.frame_material,
        color= form.color,
        image= form.image,
        quantity= form.quantity
        )
    logger.debug(f"Adding glasses: '{glasses.name}'")
    try:
        # Creating a connection to the database
        session = Session()
        # Adding glasses
        session.add(glasses)
        # Executing the command to add a new glasses to the table
        session.commit()
        logger.debug(f"Added glasses: '{glasses.name}' in the database")
        return show_glasses(glasses), 200

    except IntegrityError as e:
        error_msg = str(e)
        # checks if IntegrityError is with fk_tier_glasses constraint defined model/glasses
        if "FOREIGN KEY constraint failed" in error_msg:
            error_msg = "Sorry, choose an exist tier to associate with the glasses"
        else:
            # assuming that the other IntegrityError is duplicate problem
            error_msg = "Sorry, but we already have a glasses with this name."

        logger.warning(f"Error while trying to add glasses '{glasses.name}', {error_msg}")
        return {"msg": error_msg}, 409

    except Exception as e:
        # In case of an unexpected error
        error_msg = "Sorry but was not possible to add the new glasses"
        logger.warning(f"Unexpected while trying to add glasses '{glasses.name}', {error_msg}")
        return {"msg": error_msg}, 400


@app.get('/all_glasses', tags=[glasses_tag],
         responses={"200": ListGlassesSchema, "404": ErrorSchema})
def get_all_glasses():
    """
        Performs a search for all registered Glasses
        Returns a representation view of the glasses list
    """
    logger.debug(f"Collecting glasses")
    # Creating a connection to the database
    session = Session()
    # Performing the search
    glasses = session.query(Glasses).all()

    if not glasses:
        # If there are no glasses registered in the database
        return {"all_glasses": []}, 200
    else:
        logger.debug(f"%d glasses found" % len(glasses))
        # Returns the representation view of the glasses list
        print(glasses)
        return show_all_glasses(glasses), 200


@app.get('/glasses', tags=[glasses_tag],
         responses={"200": GlassesViewSchema, "404": ErrorSchema})
def get_glasses(query: SearchGlassesByNameSchema):
    """
        Performs the search for a Glasses based on the name of it
        Returns a representation view of:
        the glasses 
        with their associated comments
        with their the associated tier
    """
    glasses_name = query.name
    logger.debug(f"Collecting data about glasses: #{glasses_name}")
    # Creating a connection to the database
    session = Session()
    # Performing the search
    glasses = session.query(Glasses).filter(Glasses.name == glasses_name).first()

    if not glasses:
        # If the specified glasses was not found
        error_msg = "Sorry, but glasses were not found in the database "
        logger.warning(f"Error while trying to search for glasses: '{glasses_name}', {error_msg}")
        return {"msg": error_msg}, 404
    else:
        logger.debug(f"Glasses found: '{glasses.name}'")
        # Returns a representation view of glasses
        return show_glasses(glasses), 200


@app.delete('/glasses', tags=[glasses_tag],
            responses={"200": GlassesDelSchema, "404": ErrorSchema})
def del_glasses(query: SearchGlassesByNameSchema):
    """
        Deletes a Glasses based on the provided glasses name
        Returns a confirmation message of the removal
    """
    glasses_name = unquote(unquote(query.name))
    print(glasses_name)
    logger.debug(f"Deleting data about glasses: #{glasses_name}")
    # Creating a connection to the database
    session = Session()
    # Performing the search
    count = session.query(Glasses).filter(Glasses.name == glasses_name).delete()
    session.commit()

    if count:
        # Returns the representation of the confirmation msg
        logger.debug(f"Glasses: #{glasses_name} deleted.")
        return {"msg": "Glasses deleted", "id": glasses_name}
    else:
        # If the glasses was not found
        error_msg = "Glasses not found in the database"
        logger.warning(f"Error while trying to delete glasses #'{glasses_name}', {error_msg}")
        return {"msg": error_msg}, 404


@app.post('/review', tags=[review_tag],
          responses={"200": GlassesViewSchema, "404": ErrorSchema})
def add_review(form: ReviewSchema):
    """
        Adds a new review to a glasses registered in the database identified by the id
        Returns a representation of the glasses and associated comments
    """
    glasses_id  = form.glasses_id
    logger.debug(f"Adding reviews to the glasses: #{glasses_id}")
    # Creating a connection to the database
    session = Session()
    # Performing the glasses search
    glasses = session.query(Glasses).filter(Glasses.id == glasses_id).first()

    if not glasses:
        # If the glasses was not found
        error_msg = "Sorry, but glasses were not found in the database"
        logger.warning(f"Error while trying to add review to a glasses: '{glasses_id}', {error_msg}")
        return {"msg": error_msg}, 404

    # Creating a review object
    text = form.text
    stars= form.stars
    review = Review(text= text, stars=stars)
    
    # Adding the review to the speficified glasses
    glasses.add_review(review)
    session.commit()

    logger.debug(f"Adding new review to the glasses: #{glasses_id}")

    # Returns a representation view of glasses with this new review
    return show_glasses(glasses), 200
