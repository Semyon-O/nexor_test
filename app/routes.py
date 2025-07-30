from flask import Blueprint, jsonify
from app.models import Product, Category
from datetime import datetime
import logging

bp = Blueprint('main', __name__)


@bp.route('/info')
def product_info():
    try:
        products_stats = {
            'total': Product.query.count(),
            'on_main': Product.query.filter_by(on_main=True).count(),
            'regular': Product.query.filter_by(on_main=False).count()
        }

        categories = []
        for cat in Category.query.all():
            categories.append({
                'id': cat.id,
                'name': cat.name,
                'product_count': len(cat.products),
                'image_url': cat.image_url
            })

        return jsonify({
            'status': 'success',
            'data': {
                'products': products_stats,
                'categories': categories,
                'last_updated': datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        logging.exception("Error in product_info endpoint")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500