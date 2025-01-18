'''Configuration for invoking a model'''
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

class ModelConfig:
    def __init__(self, model_id, api_key, project_id, url):
        self.model_id = model_id
        self.api_key = api_key
        self.project_id = project_id
        self.url = url
        self.params = {"max_tokens": 70}

    def get_model(self):
        """Return model configuration details."""
        credentials = Credentials(url=self.url, api_key=self.api_key)
        return ModelInference(
            model_id=self.model_id,
            credentials=credentials,
            project_id=self.project_id,
            params=self.params
        )
