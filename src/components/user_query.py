'''Providing user uploaded image & query to model and getting model response'''
import base64
from src.components.api_call import ApiCall
from src.components.model_config import ModelConfig

class UserQUERY:
    def __init__(self, model_config):
        self.model = model_config.get_model()

    def passTOLLM(self, summary, query):
        content = f"summary: {summary} \n query: {query}"
        print(content) 
        messages = ApiCall.augment_api_request_body_LLM(content)
        response = self.model.chat(messages=messages)
        return response['choices'][0]['message']['content']
    
    def answer_a_question(self, content, query):
        content = f"Document content: {content} \n query: {query}"
        print(content) 
        messages = ApiCall.augment_api_request_body_doc(content)
        response = self.model.chat(messages=messages)
        return response['choices'][0]['message']['content']