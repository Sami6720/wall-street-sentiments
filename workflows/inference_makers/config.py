import os


class Config:
    """Config class"""

    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.predictions_destination_prefix = os.getenv("PREDICTIONS_DESTINATION_PREFIX")
        self.xgboost_model_path = os.getenv("XGBOOST_MODEL_PATH")
        self.random_forest_model_path = os.getenv("RANDOM_FOREST_MODEL_PATH")
