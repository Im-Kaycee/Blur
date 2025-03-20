web: daphne -b 0.0.0.0 -p $PORT blur.asgi:application
worker: celery -A blur worker --loglevel=info
beat: celery -A blur beat --loglevel=info
