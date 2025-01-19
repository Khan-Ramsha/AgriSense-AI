'''The `augment_api_request_body` function takes the user query and image as parameters and augments the body of the API request.'''

class ApiCall:
    
    def load_preprocessed_text(text_content):
   
        temp_file_path = 'src/assets/temp_text_file.txt'
        with open(temp_file_path, 'w') as file:
             file.write(text_content)
        return temp_file_path 
    @staticmethod   
    def augment_api_request_body(user_query, image):
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are an intelligent vision-based assistant specialized in agricultural diagnostics and guidance. "
                            "Your task is to analyze the provided plant image, which may depict a healthy, diseased, or abnormal plant. "
                            "Provide an accurate, concise response in 1–2 sentences to address the user's query: " + user_query
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                    },
                    
                ],
              
            }
        ]
        return messages
    
    @staticmethod
    def augment_pdf_messages(user_query, preprocessed_text):
        messages = [
            {
                "role": "user",
                "content":[
                     {
                        "type": "text",
                        "text": (
                            "You are an intelligent vision-based assistant specialized in agricultural diagnostics and guidance. "
                            "Before answering, carefully read the full context provided below. "
                            "Your task is to summarize the information and key insights in 2-3  concise bullet points, ensuring all critical details are covered. "
                            "Avoid redundant or irrelevant information. "
                            "If any query is included, make sure your points directly address the user's needs:\n\n " 
                           f"{preprocessed_text}\n\nUser Query: {user_query}" 
                            
                        )
                    },
                   
                ]
            }
        ]
        return messages
