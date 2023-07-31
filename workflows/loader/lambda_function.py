import logging

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from cloud_interactions import get_data_from_s3
from config import Config

config = Config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("loader")

client = MongoClient(config.db_connection_string,
                     server_api=ServerApi(version='1'))
db = client[config.db_name]


def lambda_handler(event, context):
    """
    Lambda handler function for loader

    :param event: Event data passed to function.
    :type: dict
    :param context: Runtime information passed to function.
    :type: dict
    """

    logger.info("The loader lambda function has started.")

    collection_name = config.get_collection_name(event['COLLECTION_NAME_SECRET_IDENTIFIER'])
    collection = db[collection_name]
    data = get_data_from_s3(config.bucket_name, event['dataPath'])
    collection.insert_many(data)

    logger.info(f"The loader lambda function has finished for {collection_name} collection.")

    return {
        'status': 'success',
    }
