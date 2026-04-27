# Python bazaviy tasviri
FROM python:3.11-slim

# Muhit o'zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ishchi katalogni yaratish
WORKDIR /app

# Tizim paketlarini o'rnatish (Postgres va boshqalar uchun)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Bog'liqliklarni o'rnatish
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Loyiha fayllarini nusxalash
COPY . /app/

# Entrypoint skriptini sozlash
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Portni ochish
EXPOSE 8000

# Entrypointni belgilash (sh orqali ishga tushirish xatoliklarni oldini oladi)
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

# Serverni ishga tushirish (Render.com uchun $PORT o'zgaruvchisidan foydalanamiz)
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT



