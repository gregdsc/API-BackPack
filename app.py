#!/usr/bin/env python

from flask import Flask
from flask_restful import Api
from resources import UserListRessource, UserResource, InterestPointListRessource, InterestPointRessource, GetToken
from activity import *
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


# User #
api.add_resource(UserListRessource, '/', '/users', '/users/', endpoint='users')
api.add_resource(UserResource, '/user/<string:id>', endpoint='user')

# Poi #
api.add_resource(InterestPointListRessource, '/pois', '/pois/', endpoint='pois')
api.add_resource(InterestPointRessource, '/poi/<string:id>', endpoint='poi')
api.add_resource(InterestPointRessource, '/filter/<string:type>', endpoint= 'filter')

# Token #
api.add_resource(GetToken, '/token', endpoint='token')

# Activity #
api.add_resource(ActivityResource, '/', '/activity', '/activity/', endpoint='activity')

# Activity Calories #
api.add_resource(ActivityCalorie, '/activity/calorie/', endpoint='calorie')
api.add_resource(ActivityCalorieMax, '/activity/calorie_max', endpoint='calorie_max')
api.add_resource(ActivityCalorieDesc, '/activity/calorie_desc', endpoint='calorie_desc')
api.add_resource(ActivityCalorieMin, '/activity/calorie_min', endpoint='calorie_min')

# Activity Speeds #
api.add_resource(ActivitySpeed, '/activity/speed/', endpoint='speed')
api.add_resource(ActivitySpeedMax, '/activity/speed_max', endpoint='speed_max')
api.add_resource(ActivitySpeedDesc, '/activity/speed_desc', endpoint='speed_desc')
api.add_resource(ActivitySpeedMin, '/activity/speed_min', endpoint='speed_min')

# Activity Pas #
api.add_resource(ActivityPas, '/activity/pas/', endpoint="pas")
api.add_resource(ActivityPasMax, '/activity/pas_max', endpoint='pas_max')
api.add_resource(ActivityPasDesc, '/activity/pas_desc', endpoint='pas_desc')
api.add_resource(ActivityPasMin, '/activity/pas_min', endpoint='pas_min')

# Activity Km #
api.add_resource(ActivityKm, '/activity/km/', endpoint='km')
api.add_resource(ActivityKmMax, '/activity/km_max', endpoint='km_max')
api.add_resource(ActivityKmDesc, '/activity/km_desc', endpoint='km_desc')
api.add_resource(ActivityKmMin, '/activity/km_min', endpoint='km_min')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
