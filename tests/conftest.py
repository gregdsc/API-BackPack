import os
import pytest
from src import create_app, db
from src.User.Model.model_user import User

@pytest.fixture(scope='module')
def new_user():
    user = User(username='alexandre', mail='alexandre.pape@epiteche.eu')
    user.hash_password('alex')
    user.description = 'description test'
    user.id = 1
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(os.getenv('FLASK_CONFIG'))

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(username='alexandre', mail='alexandre.pape@epitech.eu')
    user1.hash_password('alex')
    db.session.add(user1)

    # Commit the changes for the users

    db.session.commit()
    yield db  # this is where the testing happens!

    db.drop_all()

