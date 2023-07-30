import os


class Config:
    """Config class"""

    def __init__(self):
        """Constructor"""

        self.bucket_name = os.getenv("BUCKET_NAME")
        self.transformed_predictions_destination_prefix = os.getenv("TRANSFORMED_PREDICTIONS_DESTINATION_PREFIX")
