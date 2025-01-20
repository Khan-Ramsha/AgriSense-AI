import requests
import re
import time
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEndpoint


class Summarizer:
    def __init__(self, hf_token, repo_id):
        self.hf_token = hf_token
        self.repo_id = repo_id
        self.llm = None

    def login_to_huggingface(self):
        login(token=self.hf_token)

    def load_model(self):
        self.llm = HuggingFaceEndpoint(
            repo_id=self.repo_id, 
            max_length=200, 
            temperature=0.7, 
            token=self.hf_token
        )

    def generate_summary(self, content):
        system_prompt = (
            "You are a summarizer assistant. You will receive the user query and vision model response. "
            "Your task is to summarize the conversation. Be concise: "
        )

        user_prompt = (
            f"""
            Here is the content: "{content}"
            """
        )

        prompt = system_prompt + user_prompt
        result = self.llm.invoke(prompt)
        return result