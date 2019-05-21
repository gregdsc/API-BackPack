from flask_restful import fields

activity_field = {
    'id': fields.Integer,
    'name': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'pas': fields.Integer,
    'km': fields.Float,
    'calorie': fields.Float,
    'speed': fields.Float,
    'type': fields.String,
    'uri': fields.Url('activity', absolute=True),
}

calorie_fields = {
    'id': fields.Integer,
    'calorie': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('calorie', absolute=True),
}

calorie_field = {
    'calorie': fields.Float,
    'start_time': fields.DateTime
}

speed_fields = {
    'id': fields.Integer,
    'speed': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('speed', absolute=True),
}

speed_field = {
    'speed': fields.Float,
    'start_time': fields.DateTime
}

pas_fields = {
    'id': fields.Integer,
    'pas': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('pas', absolute=True),
}

pas_field = {
    'pas': fields.Float,
    'start_time': fields.DateTime
}

km_fields = {
    'id': fields.Integer,
    'km': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('km', absolute=True),
}

km_field = {
    'km': fields.Float,
    'start_time': fields.DateTime
}