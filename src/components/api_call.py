'''The `augment_api_request_body` function takes the user query and image as parameters and augments the body of the API request.'''

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
                            "You are an intelligent vision-based assistant specialized in agricultural diagnostics and guidance. "
                            "Your task is to analyze the provided plant image, which may depict a healthy, diseased, or abnormal plant. "
                            "Provide an accurate, concise response in 1–2 sentences to address the user's query: " + user_query
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                    }
                ]
            }
        ]
        return messages
