import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Базовые настройки
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Настройки БД
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # Интервал обновления (сек)
    UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 3600))

    # Логирование
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')