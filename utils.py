from pymongo import MongoClient
import config
import logging


def get_topics():
    client = MongoClient(config.mongo_dsn)
    db = client['pronto']
    masters = db['masters']
    fcm_topics_cursor = masters.aggregate([
        {'$match': {'email': {'$in': config.email}}},
        {'$project': {'fcmTopic': 1}}
    ])
    fcm_topics = []
    for fcm_topic in fcm_topics_cursor:
        if 'fcmTopic' in fcm_topic:
            fcm_topics.append(fcm_topic['fcmTopic'])

    return fcm_topics


def get_logger():
    logging.basicConfig(filename='sent.log', format='%(asctime)s %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger.info

