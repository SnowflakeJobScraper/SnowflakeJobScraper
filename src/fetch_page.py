# pylint: disable=W1203,C0114
import logging
from time import sleep

import requests
from config import (LOG_FORMAT, LOG_LEVEL, REQUEST_TIMEOUT, MAX_RETRIES)

# Logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger()

def fetch_page(session: requests.Session, url: str, attempt: int = 1) -> str | None:
    """Fetch a page and return the response text."""
    try:
        response = session.get(url=url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        if attempt <= MAX_RETRIES:
            sleep(attempt) # sleep some seconds
            return fetch_page(session, url, attempt + 1)
        else:
            logger.error(f"Request failed after {attempt} attempt(s): {e}")
            return None
