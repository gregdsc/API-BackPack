from flask_restful import fields

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password_hash': fields.String,
    'uri': fields.Url('user', absolute=True),

}

interest_field = {
    'id': fields.Integer,
    'id_user': fields.Integer(attribute='user_id'),
    'name': fields.String,
    'description': fields.String,
    'lat': fields.Float,
    'long': fields.Float,
    'username': fields.String,
    'type': fields.String,
    'rank': fields.Integer,
    'visible': fields.Boolean,
    'point_picture': fields.List(fields.String(attribute='url')),
    'uri': fields.Url('pois', absolute=True),
}