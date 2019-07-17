from flask_restful import fields, marshal

champs_feedback = {
    'id': fields.Integer,
    'username': fields.String,
    'mark': fields.Integer,
    'details': fields.String,
    'date': fields.DateTime(attribute='creation')
}

#'users': fields.List(fields.String(attribute='username')),

champs = {
    'feedback': fields.Nested(champs_feedback)
}