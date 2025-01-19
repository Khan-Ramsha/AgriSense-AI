import os
import base64
from dotenv import load_dotenv
import pytesseract
from PyPDF2 import PdfReader
import spacy

from src.components.api_call import ApiCall
from src.components.model_config import ModelConfig

temp_file_path = "src/assets/processed_text.txt"
pdf_file_path = "src/assets/Report_Medicinal.pdf"
class PDFAnalyzer:
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        try:
            reader = PdfReader(pdf_path)
            extracted_text = "\n".join(
                [page.extract_text() for page in reader.pages]
            )
            return extracted_text
        except Exception as e:
            raise RuntimeError(f"Error processing the PDF: {e}")
    @staticmethod
    def preprocess_text(text):
        nlp = spacy.load("en_core_web_sm")
        return "\n".join(
            [
                
                " ".join([token.text for token in nlp(line) if not token.is_punct])
                for line in text.split("\n")
                if line.strip()
            ]
        )
        
    @staticmethod
    def save_to_temp_file(text):
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(text)
    
    def __init__(self, model_config):
        self.model = model_config.get_model()
            
    def analyze_pdf(self, user_query, preprocessed_text):
        """Analyze PDF using the Watson model."""
        text_file = ApiCall.load_preprocessed_text(preprocessed_text)
        messages = ApiCall.augment_pdf_messages(user_query, preprocessed_text)
        response = self.model.chat(messages=messages)
        return response['choices'][0]['message']['content']
    
    def process_pdf(self, pdf_path,user_query):
        pdf_text = self.extract_text_from_pdf(pdf_path)
        cleaned_text = self.preprocess_text(pdf_text)
        self.save_to_temp_file(cleaned_text)
        print(f"Process text is here {temp_file_path}")
        response = self.analyze_pdf(user_query, cleaned_text)
        return response
    
    