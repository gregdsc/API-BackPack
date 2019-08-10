from src.Configuration.sight_engine import client_Sight
from flask import json
from src.Moderation_images.modele_moderate_images import Dectection


def moderate_image(url_image):
    output = client_Sight.check('nudity', 'wad', 'scam', 'offensive').set_url(url_image)
    j = json.loads(json.dumps(output))
    detection = Dectection(**j)
    if not detection.check_moderate(detection.nudity['raw'],
                                    detection.weapon,
                                    detection.alcohol,
                                    detection.drugs,
                                    detection.scam['prob'],
                                    detection.offensive['prob']):
        return 'erreur detection', False
    return True
