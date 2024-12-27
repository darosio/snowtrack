release: flask db upgrade
web: gunicorn app:app -b 0.0.0.0:$PORT -w 3
