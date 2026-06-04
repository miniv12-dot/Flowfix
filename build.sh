#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create the admin user (ignores error if already exists)
python manage.py createsuperuser --no-input || true

# Inject the mock data into the LIVE database
python manage.py generate_traffic