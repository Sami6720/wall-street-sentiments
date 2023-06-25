import os
import yaml


class Config:
    """Config class"""

    def __init__(self):
        self.finnhub_api_key = os.getenv("FINHUB_API_KEY")
        self.bucket_name = os.getenv("BUCKET_NAME")
