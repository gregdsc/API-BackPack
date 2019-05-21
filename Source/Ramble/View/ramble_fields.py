from flask_restful import fields

image = {
    'url': fields.String,
}

point = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'lat': fields.Float,
        'long': fields.Float,
        'username': fields.String,
        'type': fields.String,
        'date': fields.DateTime,
        'rank': fields.Integer,
        'point_picture': fields.List(fields.String(attribute='url')),
        'url': fields.Url('poi', absolute=True),
    }

point_for_url = {
    'point_picture': fields.List(fields.String(attribute='url')),
}

ramble = {
    'id': fields.Integer,
    'name': fields.String,
    'point':fields.Nested(point),
    'uri': fields.Url('rambles', absolute=True),
}


ramble_all = {
    'id': fields.Integer,
    'name': fields.String,
    'date': fields.DateTime(attribute='date_ramble'),
    'difficulty': fields.Integer,
    'travel time': fields.Float(attribute='travel_time'),
    'step number': fields.Float(attribute='step_number'),
    'point': fields.Nested(point_for_url),
    #'uri': fields.Url('rambles', absolute=True),
}