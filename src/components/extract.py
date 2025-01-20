from PyPDF2 import PdfReader

def extract_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                print(f"Warning: No text extracted from page {page_num + 1}")
        
        if not text:
            raise ValueError("No text found in the PDF.")
        return text
    except Exception as e:
        print(f"Error while extracting text from PDF: {e}")
        raise RuntimeError(f"Error processing PDF: {e}")
