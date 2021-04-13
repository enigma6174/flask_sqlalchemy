from db import db


class ItemModel(db.Model):

    # Table name where the items are stored
    __tablename__ = 'items'

    # Columns of the above table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Foreign key column of the table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # Define a relationship with the StoreModel table for foreign key
    store = db.relationship('StoreModel')

    # Initialize a record defined by 3 attributes = name, price, store_id
    # Actually there is a 4th attribute `ID` that is unique to the item
    # ID of an item is primary key column in database - gets added automatically, no need to initialize in object
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # Return a JSON representation of the initialized object
    def json(self):
        return {'name': self.name, 'price': self.price}

    # Return the record identified by the name of the item
    # The SQL query has been replaced by a function call but the inner functionality remains the same
    @classmethod
    def get_item(cls, name):
        return cls.query.filter_by(name=name).first()

    # Function call to add or update a record in the database
    # This call will be used to both INSERT and UPDATE records in the database tables
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Function call to delete an existing record from the database table
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
