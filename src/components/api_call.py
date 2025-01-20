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
                           "Analyze the plant image for health issues (diseased, abnormal, or healthy). " 
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

