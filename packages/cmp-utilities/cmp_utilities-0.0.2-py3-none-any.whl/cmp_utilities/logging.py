import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler


class Logger:
    def __init__(self) -> None:
        self.logger = None

    def get_google_logger(self, log_name, credentials, log_project=None):
        google_cloud_logging_client = google.cloud.logging.Client(
            credentials=credentials, project=log_project
        )
        google_cloud_logging_client.setup_logging()
        google_cloud_logging_handler = CloudLoggingHandler(
            google_cloud_logging_client, name=log_name
        )
        console_stream_handler = logging.StreamHandler()
        console_stream_handler.setLevel(logging.WARNING)
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(google_cloud_logging_handler)
        logger.addHandler(console_stream_handler)
        self.logger = logger
        return self.logger

    def get_local_logger(self, log_name):
        console_stream_handler = logging.StreamHandler()
        console_stream_handler.setLevel(logging.WARNING)
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_stream_handler)
        self.logger = logger
        return self.logger
