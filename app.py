from flask import Flask, request, jsonify, render_template, send_from_directory
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from uuid import uuid4
import os
from dotenv import load_dotenv
from src.components.model_config import ModelConfig
from src.components.plant_image_analyzer import PlantImageAnalyzer
from src.components.summary import Summarizer
from src.components.user_query import UserQUERY
from src.components.extract import extract_text
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='.')

# model config for LVM
model_config = ModelConfig(
    model_id="meta-llama/llama-3-2-11b-vision-instruct",
    api_key=os.getenv("APIKEY"),
    project_id=os.getenv("PROJECT_ID"),
    url="https://jp-tok.ml.cloud.ibm.com"
)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# model config for LLM (for generating answering user queries!)
model_config_answering = ModelConfig(
    model_id="ibm/granite-3-8b-instruct",
    api_key=os.getenv("APIKEY"),
    project_id=os.getenv("PROJECT_ID"),
    url="https://jp-tok.ml.cloud.ibm.com"
)

#creating instance
plant_analyzer = PlantImageAnalyzer(model_config)
summary_generator = Summarizer(HUGGINGFACE_TOKEN, "mistralai/Mistral-7B-Instruct-v0.3")
generating_answer = UserQUERY(model_config_answering)

authenticator = IAMAuthenticator(os.getenv("CLOUDANT_API_KEY"))
cloudant_client = CloudantV1(authenticator=authenticator)
cloudant_client.set_service_url("https://3809a24d-510f-4606-a021-66fd61c13d0b-bluemix.cloudantnosqldb.appdomain.cloud")

DB_NAME = "session-data"

try:
    cloudant_client.get_database_information(db=DB_NAME).get_result()
    print(f"Database '{DB_NAME}' already exists.")
except Exception as e:
    print(f"Database setup error: {e}")

@app.route('/')
def index():
    return render_template('/templates/index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route("/upload", methods=["POST"])
def upload():
    user_query = request.form.get("query")
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    session_id = str(uuid4())
    assets_folder = "src/assets"
    if not os.path.exists(assets_folder):
        os.makedirs(assets_folder)

    file_path = os.path.join(assets_folder, file.filename)
    file.save(file_path)
    if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        encoded_image = plant_analyzer.encode_image(file.read())
        response = plant_analyzer.analyze_plant_image(user_query, encoded_image)
        print(response) #response seems to be correct
    elif file.filename.lower().endswith('.pdf'):
        print(f"PDF file saved, checking content...")
        with open(file_path, 'rb') as f:
            file_content = f.read()
            print(f"PDF content length: {len(file_content)} bytes")
        
        pdf_content = extract_text(file_path)
        print(f"Extracted PDF content length: {len(pdf_content)}")
        print(pdf_content)
        #summarize the pdf content 
        summary_generator.login_to_huggingface()
        summary_generator.load_model()
        summary = summary_generator.generate_summary_pdf(pdf_content)
        print(user_query)
        print(summary)
        #sending summary + user_query to LLM

    else:
        return jsonify({"error": "Unsupported file type"}), 400
    print(f"User asked query: {user_query} \n Response from LVM: {response}")#correct output
    content = f"User asked query: {user_query} \n Response from LVM: {response}"
    summary_generator.login_to_huggingface()
    summary_generator.load_model()
    summary = summary_generator.generate_summary(content)
    print(summary)

    session_data = {
        "session_id": session_id,
        "summary": summary
    }
    print(session_data)
    try:
        cloudant_client.post_document(db=DB_NAME, document=session_data).get_result()
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Failed to store session data: {str(e)}"}), 500

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query")
    session_id = data.get("session_id")

    if not query or not session_id:
        return jsonify({"error": "Missing query or session_id"}), 400

    try:
        session_doc = cloudant_client.get_document(db=DB_NAME, doc_id=session_id).get_result()
        summary = session_doc.get("summary", "")
        response = generating_answer.passTOLLM(summary, query) #pass this to LLM
        print(f"Response from Model: {response}")

        content = f"User asked query: {query} \n Response from LVM: {response} \n User's conversation history so far: {summary}"

        summary_generator.login_to_huggingface()
        summary_generator.load_model()
        new_summary = summary_generator.generate_summary(content) 
        session_doc["summary"] = new_summary

        cloudant_client.put_document(db=DB_NAME, doc_id=session_id, document=session_doc).get_result()

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)