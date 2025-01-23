# AgriSense-AI 🌱

## Overview
AgriSense-AI is an innovative agricultural assistance application that leverages cutting-edge AI technologies to provide comprehensive plant care and farming insights. By integrating advanced vision and language models, the app offers intelligent, context-aware support for farmers and plant enthusiasts.

## Key Features

### 🖼️ Disease Detection
- Utilize IBM Watson's Vision Models for precise plant disease identification
- Upload images for instant, accurate diagnostic analysis

### 📄 Document Intelligence
- Upload plant-related documents
- Ask context-specific questions using advanced language models
- Extract valuable insights from uploaded materials

### 💬 Intelligent Conversations
- Maintain context-aware conversation sessions
- Leverage session history for more meaningful interactions

### 🔊 Audio Assistance
- Convert textual responses to audio using IBM Text-to-Speech service
- Enhance accessibility and user experience

## Technology Stack

### Backend
- **Framework**: Flask
- **Database**: IBM Cloudant

### AI Technologies
- **Vision Analysis**: IBM Watson Language & Vision Models
- **Natural Language Processing**: 
  - IBM Granite Model
  - Meta Llama Model
- **Speech**: IBM Text-to-Speech Service

## Prerequisites

### System Requirements
- Python 3.8+
- Active IBM Cloud account
- 
### Installation

1. Clone the repository:

   ``` bash
   https://github.com/Ayaan-tech/AgriSense-AI.git
   ```
   ``` bash
       cd IntelliBot
   ```

2. Install the dependencies:

    ```bash 
    pip install -r requirements.txt
    ```

3. Create a .env file and add your API keys & URL, Refer to .env.example file.
  
4. Run the app:

     ```bash
        python app.py
      ```
  
The app will be available at 
   ```bash
      http://127.0.0.1:5000/
   ```
### Usage

1. Upload an image or document along with a query to start the interaction.


2. Ask follow-up questions without re-uploading the file.


3. Listen to audio responses generated by the app.











