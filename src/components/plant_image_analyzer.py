'''Providing user uploaded image & query to model and getting model response'''
import base64
from src.components.api_call import ApiCall
from src.components.model_config import ModelConfig

class PlantImageAnalyzer:
    def __init__(self, model_config):
        self.model = model_config.get_model()

    @staticmethod
    def encode_image(image_bytes: bytes):
        """encoding and decoding"""
        return base64.b64encode(image_bytes).decode("utf-8")

    def analyze_plant_image(self, user_query, encoded_image):
        """Analyze plant image using the Watson model."""
        
        messages = ApiCall.augment_api_request_body(user_query, encoded_image)
        response = self.model.chat(messages=messages)
        return response['choices'][0]['message']['content']
