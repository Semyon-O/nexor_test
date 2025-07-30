from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    register_models(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    init_scheduler(app)

    return app

def register_models(app):
    with app.app_context():
        from app.models import Product, Category, ProductParameter, ProductCategory
        db.create_all()
        print("Таблицы успешно созданы")

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: update_products(app),
        trigger='interval',
        seconds=app.config['UPDATE_INTERVAL']
    )
    scheduler.start()

def update_products(app):
    with app.app_context():
        from app.tasks import load_products
        load_products()