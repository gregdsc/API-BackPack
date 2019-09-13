web: gunicorn --limit-request-line 0 app:app

release: python manager.py db upgrade
