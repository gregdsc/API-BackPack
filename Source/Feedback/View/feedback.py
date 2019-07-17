from Source.Feedback.Model.model_feedback import *
from Source.Point.View.interest_point import *
from Source.Authentification.token import *
from Source.Authentification.Bearer import *


class feedback(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mark', type=int)
    parser.add_argument('details', type=str)

    @authToken.login_required
    def post(self):
        parsed_args = self.parser.parse_args()
        details = parsed_args['details']
        mark = parsed_args['mark']
        date = datetime.datetime.now()
        feedback = Feedback(details=details, mark=mark, username=g.current_user.username,
                          creation_date=date)
        session.add(feedback)
        session.commit()
        description_html = """\
<html>
  <head></head>
  <body>
    <h1 style="color: #5e9ca0;">Nouveau Feedback de&nbsp;""" + str(feedback.username) + """</h1>
    <h2 style="color: #2e6c80;">rank: """ + str(feedback.mark) + """</h2>
    <h2 style="color: #2e6c80;">Description: """ + str(feedback.details) + """</h2>
  </body>
</html>
"""
        send_mail('noreply.backpack@gmail.com', 'test du mail', ['gregoire.descombris@epitech.eu'], render_template("template_feedback.html"))
        return 201