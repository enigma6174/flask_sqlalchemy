from app import app
from db import db

db.init_app(app)


# Instruction to SQLAlchemy to create tables and database before any queries are executed
@app.before_first_request
def create_tables():
    db.create_all()
