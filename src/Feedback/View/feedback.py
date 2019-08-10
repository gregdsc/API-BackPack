from flask import render_template
from flask_restful import reqparse, Resource
from src.Feedback.Model.model_feedback import Feedback
from src.Authentification.authentification import authToken
from src.Configuration.session import session
import datetime
from src.Email.send_email import send_mail

from flask_restful import abort


class FeedbackUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mark', type=int)
    parser.add_argument('details', type=str)

    @authToken.login_required
    def post(self):
        parsed_args = self.parser.parse_args()
        details = parsed_args['details']
        mark = parsed_args['mark']
        date = datetime.datetime.now()

        if details is None or mark is None:
            abort(400, message="Missing arguments")
        if mark < 1 or mark > 5:
            abort(400, message="The mark should be between 1 to 5")
        else:
            feedback = Feedback(details=details, mark=mark, username=g.current_user.username,
                                creation_date=date)
            session.add(feedback)
            session.commit()
            try:
                send_mail('noreply.backpack@gmail.com', 'Nouveau Feedback',
                          ['gregoire.descombris@epitech.eu'], render_template("template_feedback.html",
                                                                              user_name=feedback.username,
                                                                              mark=feedback.mark,
                                                                              details=feedback.details))
            except:
                abort(400, message='mail non envoyé')
            return 201
