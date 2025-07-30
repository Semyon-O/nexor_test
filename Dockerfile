FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn==20.1.0 && \
    pip install psycopg2

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PORT=5555

RUN mkdir -p /app/logs

CMD ["gunicorn", "--bind", "0.0.0.0:5555", "--workers", "4", "wsgi:app"]