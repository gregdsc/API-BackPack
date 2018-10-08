#!/usr/bin/env python

from flask import Flask
from flask_restful import Api
from resources import UserListRessource, UserResource, InterestPointListRessource, InterestPointRessource, GetToken
from activity import ActivityResource, ActivityCalorie, ActivitySpeed
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
api.add_resource(ActivityCalorie, '/activity/calorie/', endpoint='calorie')
api.add_resource(ActivitySpeed, '/activity/speed/', endpoint='speed')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
