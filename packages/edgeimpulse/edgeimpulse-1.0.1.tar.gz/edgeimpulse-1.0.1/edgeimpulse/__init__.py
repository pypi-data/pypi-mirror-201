import edgeimpulse.model
import edgeimpulse.exceptions

import os

__version__ = "0.1.0"

try:
    API_KEY = os.environ["EI_API_KEY"]
except KeyError:
    API_KEY = None

try:
    API_ENDPOINT = os.environ["EI_API_ENDPOINT"]
except KeyError:
    API_ENDPOINT = "https://studio.edgeimpulse.com/v1"
