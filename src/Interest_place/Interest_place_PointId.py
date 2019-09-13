import pprint

from flask import json
from flask_restful import Resource
from src.Point.View.interest_point_id import PointId
from src.Interest_place.Interest_place import place_point_POI


class Point_places(Resource):
    def get(self, id_point):
        poi = PointId.get(self, id_point)
        #print(poi['long'])
        #print(poi['lat'])
        #print(type(place_point_POI((str(poi['long'])), str(poi['lat']))))
        return place_point_POI((str(poi['long'])), str(poi['lat']))
