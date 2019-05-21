from flask_restful import fields, marshal

interest_field = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'lat': fields.Float,
    'long': fields.Float,
    'userName': fields.String,
    'type': fields.String,
    'rank': fields.Integer,
    'imageUrls': fields.List(fields.String(attribute='url')),
    'uri': fields.Url('poi', absolute=True),
}