#!/bin/sh

# Migratsiyalarni amalga oshirish
echo "Migratsiyalar bajarilmoqda..."
python manage.py migrate --noinput


# Statik fayllarni yig'ish
echo "Statik fayllar yig'ilmoqda..."
python manage.py collectstatic --noinput

# Serverni ishga tushirish
echo "Server ishga tushmoqda..."
exec "$@"
