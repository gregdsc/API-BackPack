from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import os

from Source import create_app

app = create_app(os.getenv('FLASK_CONFIG'))

with app.app_context():
    from Source.Ramble.Model.model_ramble import *
    from Source.User.Model.model_user import *
    from Source.Point.Model.model_point import *
    from Source.Activity.Model.model_activity import *
    from Source.Comment.Model.model_comment import *


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
