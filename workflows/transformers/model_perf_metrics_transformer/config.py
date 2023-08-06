import os


class Config:
    """Config class"""

    def __init__(self):

        self.log_level = os.getenv("LOG_LEVEL", default="DEBUG")

        self.bucket_name = os.getenv("BUCKET_NAME", 'stock-sentiment-data-sami')
        self.model_perf_metrics_destination_prefix = os.getenv(
            "MODEL_PERF_METRICS_DESTINATION_PREFIX", 'transformed_data/model_perf_metrics')

        self.db_connection_string = os.getenv(
            "DB_CONNECTION_STRING", "mongodb+srv://wsS123-wsS124:WyETKcYAOv5HXkfA@wss-cluster.fe7gcww.mongodb.net/?retryWrites=true&w=majority")
        self.db_name = os.getenv("DB_NAME", 'wss_db')
        self.db_collection_name = os.getenv("MODEL_PERF_METRICS_COLLECTION_NAME", 'model_perf_metrics')

        self.aggregation_pipeline = [
            {
                "$group": {
                    "_id": "$model",
                    "historic_buy_predictions_profit": {
                        "$sum": "$buy_predictions_profit"
                    },
                    "historic_not_buy_predictions_save": {
                        "$sum": "$not_buy_predictions_save"
                    },
                    "total_buy_predictions_count": {
                        "$sum": "$buy_predictions_count"
                    },
                    "total_not_buy_predictions_count": {
                        "$sum": "$not_buy_predictions_count"
                    },
                    "total_correct_buy_predictions_count": {
                        "$sum": "$correct_buy_predictions_count"
                    },
                    "total_correct_not_buy_predictions_count": {
                        "$sum": "$correct_not_buy_predictions_count"
                    },
                    "total_good_days_money_wise": {
                        "$sum": "$good_day_money_wise"
                    },
                    "total_good_days_accuracy_wise": {
                        "$sum": "$good_day_accuracy_wise"
                    },
                    "total_days": {
                        "$sum": 1
                    }
                }
            }
        ]

        self.aggregated_metrics_by_models_column_names = [
            "model", "historic_buy_predictions_profit", "historic_not_buy_predictions_save",
            "total_buy_predictions_count", "total_not_buy_predictions_count", "total_correct_buy_predictions_count",
            "total_correct_not_buy_predictions_count", "total_good_days_money_wise", "total_good_days_accuracy_wise",
            "total_days"
        ]
