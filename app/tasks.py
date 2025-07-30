import requests
from datetime import datetime
from app import db
from app.models import Product, Category, ProductParameter, ProductCategory
import logging


def load_products():
    """Основная функция загрузки и объединения данных"""
    try:
        logging.info("Starting products data update")

        api1_url = "https://bot-igor.ru/api/products?on_main=true"
        api2_url = "https://bot-igor.ru/api/products?on_main=false"

        api1_data = requests.get(api1_url).json()
        api2_data = requests.get(api2_url).json()

        all_products = api1_data.get('products', []) + api2_data.get('products', [])

        process_categories(api1_data.get('categories', []))

        for product_data in all_products:
            process_product(product_data)

        db.session.commit()
        logging.info(f"Successfully updated {len(all_products)} products")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to update products: {str(e)}")
        raise


def process_categories(categories_data):
    """Обновление категорий в БД"""
    existing_ids = {c[0] for c in db.session.query(Category.id).all()}

    for cat_data in categories_data:
        if cat_data['Category_ID'] not in existing_ids:
            category = Category(
                id=cat_data['Category_ID'],
                name=cat_data['Category_Name'],
                image_url=cat_data['Category_Image']
            )
            db.session.add(category)


def process_product(product_data):
    """Обработка товара с проверкой дат"""
    try:
        # Проверка и парсинг дат
        created_at = parse_date(product_data['Created_At'])
        updated_at = parse_date(product_data.get('Updated_At')) if product_data.get('Updated_At') else created_at

        product = Product(
            id=product_data['Product_ID'],
            name=product_data['Product_Name'],
            created_at=created_at,
            updated_at=updated_at,
            on_main=product_data['OnMain'],
            main_image_url=get_main_image(product_data.get('images', []))
        )

        # Используем merge для обновления существующих записей
        db.session.merge(product)

        # Обработка связей и параметров
        process_product_associations(product_data, product.id)

    except Exception as e:
        logging.error(f"Error processing product {product_data.get('Product_ID')}: {str(e)}")
        db.session.rollback()


def process_product_associations(product_data, product_id):
    db.session.query(ProductCategory).filter_by(product_id=product_id).delete()
    for cat_data in product_data.get('categories', []):
        pc = ProductCategory(
            product_id=product_id,
            category_id=cat_data['Category_ID']
        )
        db.session.merge(pc)

    db.session.query(ProductParameter).filter_by(product_id=product_id).delete()
    for param_data in product_data.get('parameters', []):
        param = ProductParameter(
            id=param_data['Parameter_ID'],
            name=param_data['name'],
            value=param_data['parameter_string'],
            price=float(param_data['price']),
            old_price=float(param_data['old_price']) if param_data.get('old_price') else None,
            product_id=product_id
        )
        db.session.merge(param)

def parse_date(date_str):
    if not date_str:
        return datetime.utcnow()
    try:
        return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
    except ValueError:
        return datetime.utcnow()


def get_main_image(images):
    for img in images:
        if img.get('MainImage'):
            return img['Image_URL']
    return None