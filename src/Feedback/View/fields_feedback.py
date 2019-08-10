from flask_restful import fields

champs_feedback = {
    'id': fields.Integer,
    'username': fields.String,
    'mark': fields.Integer,
    'details': fields.String,
    'date': fields.DateTime(attribute='creation')
}

champs = {
    'feedback': fields.Nested(champs_feedback)
}