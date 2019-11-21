#!/usr/bin/env python
from flask_restful import Api
from src.User.View.user import Utilisateur
from src.User.View.user_id import UtilisateurId
from src.User.View.reset_password import Reset_Password
from src.Point.View.point_user import UserPoi
from src.Point.View.interest_point import Point
from src.Point.View.interest_point_id import PointId
from src.Point.View.interest_point_filtre import PointFiltre
from src.Point.View.point_visible_user import PointVisibleUser
from src.Authentification.token import GetToken
from src.Ramble.View.ramble import RambleRessource
from src.Ramble.View.ramble_id import RambleId
from src.Ramble.View.pointinramble import PointInRamble
from src.Comment.View.comment import UserComment, CommentPoint
from src.Feedback.View.feedback import FeedbackUser
from src.History.View.history import HistoriqueDate, HistoriqueRank
from src.Prevision_images.prevision_image import PrevisionImage
from src.Interest_place.Interest_place_PointId import Point_places
from src import create_app

import os

api = Api()

# User #
api.add_resource(Utilisateur, '/', '/users', '/users/', endpoint='users')
api.add_resource(UtilisateurId, '/user/<int:id>', endpoint='user')

# Reset_password #
api.add_resource(Reset_Password, '/reset_password', '/reset_password/', endpoint='reset_password')

# Poi user #
api.add_resource(UserPoi, '/pois_me', '/pois_me/', endpoint='pois_me')
api.add_resource(UserPoi, '/poi_me/<string:id>', '/poi_me/<string:id>', endpoint='poi_me')


# Poi #
api.add_resource(Point, '/pois', '/pois/', endpoint='pois')
api.add_resource(PointId, '/poi/<int:id_point>', endpoint='poi')
api.add_resource(PointFiltre, '/filter/<string:type>', endpoint='filter')
api.add_resource(PointVisibleUser, '/poi_visible/<int:id>', endpoint='poi_visible')

# Poi Places #

api.add_resource(Point_places, '/poi_places/<int:id_point>', endpoint='poi_places')

# Token #
api.add_resource(GetToken, '/token', endpoint='token')


# Ramble #
api.add_resource(RambleRessource, '/ramble', '/ramble/', endpoint='ramble')

# Ramble ID #

api.add_resource(PointInRamble, '/ramble_point/<int:id>/<int:id_point>', endpoint='ramble_point')
api.add_resource(RambleId, '/rambles/<int:id>', endpoint='rambles')

# Comment #

api.add_resource(UserComment, '/comments', '/comments/', endpoint='comments')
api.add_resource(UserComment, '/comment/<int:id>', endpoint='comment')
api.add_resource(CommentPoint, '/comment/point_interet/<int:id_poi>', endpoint='point_interet')

# Feedback #

api.add_resource(FeedbackUser, '/feedback', '/feedback/', endpoint='feedback')

# History

api.add_resource(HistoriqueDate, '/history/date', endpoint='date')
api.add_resource(HistoriqueRank, '/history/rank', endpoint='rank')

# Prevision

api.add_resource(PrevisionImage, '/prevision', '/prevision/', endpoint='prevision')

app = create_app(os.getenv('FLASK_CONFIG'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
