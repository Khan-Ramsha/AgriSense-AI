class ApiCall:
    @staticmethod
    def augment_api_request_body(user_query, image):
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                           "Analyze the plant image for health issues(diseased, abnormal, or healthy). " 
                           "Answer to user's question concisely: " + user_query    )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                    }
                ]
            }
        ]
        return messages

    @staticmethod
    def augment_api_request_body_LLM(content):
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ("You are a plant expert assistant.Answer the user's plant-related query using their conversation history:" + content)
                    }
                ]
            }
        ]
        return messages

    @staticmethod
    def augment_api_request_body_doc(content):
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ("You are a plant expert assistant.Answer the user's plant-related query using the document content:" + content)
                    }
                ]
            }
        ]
        return messages