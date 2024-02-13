import os


class Config():
    """
    Class to store configuration variables.
    """

    def __init__(self) -> None:
        self.db_connection_string = os.environ['DB_CONNECTION_STRING']
        self.db_name = os.environ['DB_NAME']
        self.collection_name = os.environ['MODEL_PERF_METRICS_COLLECTION_NAME']
