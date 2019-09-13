web: gunicorn app:app --limit-request-line 0
release: python manager.py db upgrade
