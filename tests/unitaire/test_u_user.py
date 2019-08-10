
from src.User.Model.model_user import UserPicture



def test_new_user(new_user):
    assert new_user.username == 'alexandre'
    assert new_user.username != 'alexandre_test'
    assert new_user.mail == 'alexandre.pape@epiteche.eu'
    assert new_user.password_hash != 'alex'
    assert new_user.description == 'description test'


def test_new_user_password(new_user):
    new_user.hash_password('alex')
    assert new_user.password_hash != 'alex'
    assert new_user.verify_password('alex')
    assert not new_user.verify_password('alex2')


def test_ajout_photo_user(new_user):
    user_picture = UserPicture(id=1, user_id=new_user.id, url='https://url_cloudinary')
    assert user_picture.id == 1
    assert user_picture.user_id == new_user.id
    assert user_picture.url == 'https://url_cloudinary'
    assert not user_picture.url == 'https://url_cloudinary_FAKE'
