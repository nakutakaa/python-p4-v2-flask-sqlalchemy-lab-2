# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin


# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)


# class Customer(db.Model):
#     __tablename__ = 'customers'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)

#     def __repr__(self):
#         return f'<Customer {self.id}, {self.name}>'


# class Item(db.Model):
#     __tablename__ = 'items'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     price = db.Column(db.Float)

#     def __repr__(self):
#         return f'<Item {self.id}, {self.name}, {self.price}>'
    
# class Review(db.Model):
#     __tablename__ = 'reviews'

#     id = db.Column(db.Interger, primary_key=True)
#     comment = db.Column(db.string)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
#     item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin): # Added SerializerMixin here for future tasks
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationships
    # A customer has many reviews
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    # allows a Customer object to directly access the 'item' objects
    # that are associated with its 'reviews'.
    # It proxies through the 'reviews' relationship, accessing the 'item' attribute of each review.
    items = association_proxy('reviews', 'item')

    # Exclude reviews.customer to prevent recursion
    serialize_rules = ('-reviews.customer',)



    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin): # Added SerializerMixin here for future tasks
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationships
    # An item has many reviews
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    # Exclude reviews.item to prevent recursion
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin): # Added SerializerMixin here for future tasks
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String) # Corrected 'string' to 'String'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationships
    # A review belongs to one customer
    customer = db.relationship('Customer', back_populates='reviews')
    # A review belongs to one item
    item = db.relationship('Item', back_populates='reviews')
    # Exclude customer.reviews and item.reviews to prevent recursion
    serialize_rules = ('-customer.reviews', '-item.reviews',)


    def __repr__(self):
        return f'<Review {self.id}, Customer ID: {self.customer_id}, Item ID: {self.item_id}>'

