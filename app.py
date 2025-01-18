#imports
import requests
import base64
import getpass
from PIL import Image
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv

load_dotenv()

WATSONX_EU_APIKEY = os.getenv("APIKEY")
WATSONX_EU_PROJECT_ID = os.getenv("PROJECT_ID")

URL = "https://us-south.ml.cloud.ibm.com"

