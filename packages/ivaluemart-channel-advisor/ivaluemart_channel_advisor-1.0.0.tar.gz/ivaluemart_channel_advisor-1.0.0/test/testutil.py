import os

import google.cloud.logging
import logging


def setup_logging(level=logging.INFO):
    logger = logging.getLogger('root')
    logger.setLevel(level)
    if 'IS_APPENGINE' in os.environ and os.environ['IS_APPENGINE'] == 'true':
        client = google.cloud.logging.Client()
        client.setup_logging()
