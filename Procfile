release:python manage.py migrate
web: gunicorn Crawler.wsgi --log-file -
celery: celery -A Crawler.cele worker -l INFO



