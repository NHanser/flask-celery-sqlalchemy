from app.extensions import db

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from app.models.feedeater_models import Feed
    from app.models.user import User, Role
    db.create_all()