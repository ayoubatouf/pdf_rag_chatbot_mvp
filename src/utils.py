import logging
import yaml
import logging.config


def setup_logging():
    with open("config/logging.yaml", "r") as f:
        logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)


def load_config(config_path="config/config.yaml"):
    try:
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
            logging.info("Config loaded successfully.")
            return config
    except Exception as e:
        logging.error(f"Error loading config file: {str(e)}")
        raise
