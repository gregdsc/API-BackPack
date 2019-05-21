from flask_restful import fields, marshal

champs_comment = {
    'id': fields.Integer,
    'username': fields.String,
    'details': fields.String,
    'rank': fields.Integer,
    'date': fields.DateTime(attribute='creation'),
    'last modification': fields.DateTime(attribute='derniere_modification')
}

#'users': fields.List(fields.String(attribute='username')),

champs = {
    'comment': fields.Nested(champs_comment)
}