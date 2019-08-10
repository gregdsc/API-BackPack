from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import os

from src import create_app

app = create_app(os.getenv('FLASK_CONFIG'))

with app.app_context():
    from src.Feedback.Model.model_feedback import *


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
