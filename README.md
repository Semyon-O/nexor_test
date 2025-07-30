# Старт приложения

```
git clone 
cd <папка-проекта>
```

```
При необходимости задайте нужные натсройки в Compose или через .env файл
# Настройки PostgreSQL
DB_HOST=db
DB_PORT=5432
DB_NAME=shop
DB_USER=postgres
DB_PASSWORD=postgres

# Интервал обновления данных (в секундах)
UPDATE_INTERVAL=3600  # 1 час

# Дополнительные настройки
LOG_LEVEL=INFO
 ```

```запуск
docker-compose up --build
```