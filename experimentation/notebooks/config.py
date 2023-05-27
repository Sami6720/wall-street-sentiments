import yaml


class Config:
    """Config class"""

    def __init__(self):
        # Change this to your config.yaml file path
        CONFIG_FILE_PATH = "..\..\common\config\config.yaml"
        self.load_config(config_file_path=CONFIG_FILE_PATH)

    def load_config(self, config_file_path: str) -> None:
        """Load config from config.yaml file in common/config folder
        
        param config_file_path: path to config.yaml file
        type: str
        """
        with open(config_file_path, "r", encoding='utf-8') as file:
            config = yaml.safe_load(file)

            # Reddit API config
            self.reddit_api_client = config["reddit_api_config"]["client_id"]
            self.reddit_api_secret = config["reddit_api_config"]["client_secret"]
            self.reddit_api_user_agent = config["reddit_api_config"]["user_agent"]

            # FinnHub API config
            self.finnhub_api_key = config["finnhub_api_config"]["api_key"]