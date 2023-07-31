import os


class Config:
    """Config class"""

    def __init__(self):

        self.log_level = os.getenv("LOG_LEVEL", default="DEBUG")

        self.bucket_name = os.getenv("BUCKET_NAME")
        self.model_perf_metrics_destination_prefix = os.getenv("MODEL_PERF_METRICS_DESTINATION_PREFIX")

        self.db_connection_string = os.getenv("DB_CONNECTION_STRING")
        self.db_name = os.getenv("DB_NAME")
        self.db_collection_name = os.getenv("MODEL_PERF_METRICS_COLLECTION_NAME")

        self.aggregation_pipeline = [
            {
                "$group": {
                    "_id": "$model",
                    "total_net_buy_profits": {
                        "$sum": "$net_buy_profits"
                    },
                    "total_not_buy_saves": {
                        "$sum": "$not_buy_saves"
                    },
                    "total_good_days": {
                        "$sum": "$good_day"
                    },
                    "total_days": {
                        "$sum": 1
                    }
                }
            }
        ]

        self.aggregated_metrics_by_models_column_names = [
            'model', 'historic_buy_predictions_profit', 'historic_not_buy_predictions_save',
            'total_good_days', 'total_days'
        ]
