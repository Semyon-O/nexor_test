from datetime import datetime
from app.database import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))

    products = db.relationship(
        'Product',
        secondary='product_categories',
        back_populates='categories'
    )


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    on_main = db.Column(db.Boolean, default=False)
    main_image_url = db.Column(db.String(255))

    categories = db.relationship(
        'Category',
        secondary='product_categories',
        back_populates='products'
    )
    parameters = db.relationship(
        'ProductParameter',
        backref='product',
        cascade='all, delete-orphan'
    )


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='CASCADE'),
        primary_key=True
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', ondelete='CASCADE'),
        primary_key=True
    )


class ProductParameter(db.Model):
    __tablename__ = 'product_parameters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.String(100))
    price = db.Column(db.Float)
    old_price = db.Column(db.Float)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='CASCADE')
    )