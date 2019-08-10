from flask_restful import abort


class Nudity(object):
    def __init__(self, raw, partial, safe):
        self.raw = raw
        self.partial = partial
        self.safe = safe

    raw = float
    partial = float
    safe = float


class Request(object):
    def __init__(self, id, timestamp, operation):
        self.id = id
        self.timestamp = timestamp
        self.operations = operation

    id = str
    timestamp = float
    operations = int


class Media(object):
    def __init__(self, id, uri):
        self.id = id,
        self.uri = uri

    id = str
    uri = str


class Scam(object):
    def __init__(self, prob):
        self.prob = prob

    prob = float


class Offensive(object):
    def __init__(self, prob):
        self.prob = prob

    prob = float


class Dectection(object):
    def __init__(self, status, request, nudity, media, weapon, alcohol, drugs, scam, offensive, faces):
        self.status = status
        self.request = request
        self.nudity = nudity
        self.media = media
        self.weapon = weapon
        self.alcohol = alcohol
        self.drugs = drugs
        self.scam = scam
        self.offensive = offensive
        self.faces = faces

    status = str
    request = Request
    nudity = Nudity
    media = Media
    weapon = float
    alcohol = float
    drugs = float
    scam = Scam
    offensive = Offensive
    faces = []

    @staticmethod
    def check_moderate(raw, weapon, alcohol, drugs, scam, offensive):

        if raw >= 0.5:
            abort(401, message="votre photo ne rentre pas dans les conditions général (nudité)")
        elif weapon >= 0.5:
            abort(401, message="votre photo ne rentre pas dans les conditions général (arme)")
        elif alcohol >= 0.5:
            abort(401, message="votre photo ne rentre pas dans les conditions général (alcool)")
        elif drugs >= 0.5:
            abort(401, message="votre photo ne rentre pas dans les conditions général (drogue)")
        elif offensive >= 0.5:
            abort(401, message="votre photo ne rentre pas dans les conditions général (innaproprié)")
        elif scam >= 0.5:
            abort(401, message="votre photo ne rentre pas dans les conditions général (escroc)")
        return True
