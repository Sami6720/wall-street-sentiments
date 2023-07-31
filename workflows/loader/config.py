import os


class Config():
    """
    Class to store configuration variables.
    """

    def __init__(self) -> None:
        self.bucket_name = os.environ['BUCKET_NAME']
        self.db_connection_string = os.environ['DB_CONNECTION_STRING']
        self.db_name = os.environ['DB_NAME']

    def get_collection_name(self, collection_secret_identifier: str) -> str:
        """
        Get collection name from environment variables.

        :param event: Event data passed to function.
        :type: dict
        :return: Collection name.
        :rtype: str
        """
        return os.getenv(collection_secret_identifier)
