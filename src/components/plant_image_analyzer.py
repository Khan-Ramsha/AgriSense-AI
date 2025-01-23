'''Providing user uploaded image & query to model and getting model response'''
import base64
import requests
from src.components.api_call import ApiCall
from src.components.model_config import ModelConfig
import imghdr

class PlantImageAnalyzer:
    def __init__(self, model_config):
        self.model = model_config.get_model()
    @staticmethod

    def encode_image(file_path):
        """Encode an image from a local file path to base64"""
        try:
            with open(file_path, 'rb') as image_file:
                # Return the base64 encoded image URL
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{base64_image}"
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None

    def analyze_plant_image(self, user_query, encoded_image):
        """Analyze plant image using the Watson model."""
        messages = ApiCall.augment_api_request_body(user_query, encoded_image)
        response = self.model.chat(messages=messages)
        return response['choices'][0]['message']['content']