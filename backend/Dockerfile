FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DJANGO_SETTINGS_MODULE=portfolio.settings.production python manage.py collectstatic --noinput

EXPOSE $PORT

CMD gunicorn portfolio.wsgi:application --bind=0.0.0.0:$PORT --workers=2