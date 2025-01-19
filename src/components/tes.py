### api_call.py

import base64

class ApiCall:
    @staticmethod
    def load_preprocessed_text(file_path):
        """
        Loads the preprocessed text from a file.
        """
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def augment_api_request_body(user_query, preprocessed_text):
        """
        Constructs the request body for the model API.
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You are a helpful assistant. Use the following context to answer the query in 1-2 sentences:\n\n{preprocessed_text}\n\nUser Query: {user_query}"
                    }
                ]
            }
        ]
        return messages

    @staticmethod
    def query_model_with_context(user_query, text_file, model, credentials, watson_id):
        preprocessed_text = ApiCall.load_preprocessed_text(text_file)
        messages = ApiCall.augment_api_request_body(user_query, preprocessed_text)

        model_inference = model(
            model_id="meta-llama/llama-3-2-90b-vision-instruct",
            credentials=credentials,
            project_id=watson_id,
            params={"max_tokens": 200}
        )

        response = model_inference.chat(messages=messages)
        return response

### model_config.py

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import os

class ModelConfig:
    def __init__(self, model_id, api_key, project_id, url):
        self.model_id = model_id
        self.api_key = api_key
        self.project_id = project_id
        self.url = url

    def get_model(self):
        credentials = Credentials(
            url=self.url,
            api_key=self.api_key
        )
        return ModelInference(
            model_id=self.model_id,
            credentials=credentials,
            project_id=self.project_id
        )

# Example credentials setup
if __name__ == "__main__":
    WATSONX_API = os.getenv('WATSONX_API', "your_api_key")
    WATSONX_PROJECT = os.getenv('WATSONX_PROJECT', "your_project_id")
    URL = "https://us-south.ml.cloud.ibm.com"

    config = ModelConfig(
        model_id="meta-llama/llama-3-2-90b-vision-instruct",
        api_key=WATSONX_API,
        project_id=WATSONX_PROJECT,
        url=URL
    )
    model = config.get_model()
    print("Model configuration loaded successfully.")

### pdf_analyzer.py

import os
import base64
from dotenv import load_dotenv
import pytesseract
from PyPDF2 import PdfReader
from google.colab import files
import spacy

# TEMP_FILE_PATH is used to store preprocessed text temporarily
TEMP_FILE_PATH = "/content/processed_text.txt"

class PDFAnalyzer:
    @staticmethod
    def upload_pdf():
        print("Please upload your PDF file:")
        uploaded = files.upload()
        if uploaded:
            pdf_path = list(uploaded.keys())[0]
            print(f"File uploaded successfully: {pdf_path}")
            return pdf_path
        else:
            raise ValueError("No file uploaded. Please try again.")

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        try:
            reader = PdfReader(pdf_path)
            extracted_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
                else:
                    extracted_text += "[WARNING: Text could not be extracted from this page]\n"

            return extracted_text
        except Exception as e:
            print(f"Error processing the PDF: {e}")
            return ""

    @staticmethod
    def preprocess_text(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        processed_text = "\n".join(
            [
                " ".join([token.text for token in nlp(line) if not token.is_stop and not token.is_punct])
                for line in text.split("\n")
                if line.strip()
            ]
        )
        return processed_text

    @staticmethod
    def save_to_temp_file(text):
        with open(TEMP_FILE_PATH, "w") as temp_file:
            temp_file.write(text)
        print(f"Processed text saved to {TEMP_FILE_PATH}")

    @staticmethod
    def load_from_temp_file():
        if os.path.exists(TEMP_FILE_PATH):
            with open(TEMP_FILE_PATH, "r") as temp_file:
                return temp_file.read()
        else:
            print("No previous processed text found.")
            return ""

# Example of usage
if __name__ == "__main__":
    try:
        existing_text = PDFAnalyzer.load_from_temp_file()

        if existing_text:
            print("Using previously processed text.")
            cleaned_text = existing_text
        else:
            pdf_path = PDFAnalyzer.upload_pdf()
            pdf_text = PDFAnalyzer.extract_text_from_pdf(pdf_path)
            cleaned_text = PDFAnalyzer.preprocess_text(pdf_text)
            PDFAnalyzer.save_to_temp_file(cleaned_text)

        lines = cleaned_text.split("\n")
        print("\nPreprocessed Text (First 100 lines):\n")
        for i, line in enumerate(lines[:100]):  # Print the first 100 lines
            print(f"Line {i + 1}: {line}")

    except Exception as e:
        print(f"Error: {e}")
