#!/usr/bin/env python

from flask_restful import Api
from Source.User.View.user import Utilisateur
from Source.User.View.user_id import Utilisateur_id
from Source.Authentification.token import *
from Source.Point.View.point_user import *
from Source.Point.View.interest_point import *
from Source.Point.View.interest_point_id import *
from Source.Point.View.interest_point_filtre import *
from Source.Ramble.View.ramble import *
from Source.Ramble.View.ramble_id import *
from Source.Comment.View.comment import *
from Source.History.View.history import *

from Source.__init__ import *

app = create_app(os.getenv('FLASK_CONFIG'))

api = Api(app)


# User #
api.add_resource(Utilisateur, '/', '/users', '/users/', endpoint='users')
api.add_resource(Utilisateur_id, '/user/<int:id>', endpoint='user')

# Poi user #
api.add_resource(User_Poi, '/pois_me', '/pois_me/', endpoint='pois_me')
api.add_resource(User_Poi, '/poi_me/<string:id>', '/poi_me/<string:id>', endpoint='poi_me')


# Poi #
api.add_resource(Point, '/pois', '/pois/', endpoint='pois')
api.add_resource(Point_id, '/poi/<string:id>', endpoint='poi')
api.add_resource(Point_filtre, '/filter/<string:type>', endpoint='filter')


# Token #
api.add_resource(GetToken, '/token', endpoint='token')


# Ramble #
api.add_resource(Ramble_ressource, '/ramble', '/ramble/', endpoint='ramble')

# Ramble ID #

api.add_resource(Point_in_Ramble, '/ramble_point/<int:id>/<int:id_point>', endpoint='ramble_point')
api.add_resource(Id_ramble, '/rambles/<int:id>', endpoint='rambles')

# Comment #

api.add_resource(comment, '/comments', '/comments/', endpoint='comments')
api.add_resource(comment, '/comment/<int:id>', endpoint='comment')
api.add_resource(comment_point, '/comment/point_interet/<int:id_poi>', endpoint='point_interet')


# History

api.add_resource(historique_date, '/history/date', endpoint='date')
api.add_resource(historique_rank, '/history/rank', endpoint='rank')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
