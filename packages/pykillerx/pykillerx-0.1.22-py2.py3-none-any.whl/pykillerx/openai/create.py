import requests

class PayLoadHeaders:
    def __init__(self, model, prompt, api_key):
        self.payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0,
            "top_p": 1,
            "stream": False,
            "logprobs": None,
            "stop": None
        }
        self.headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": apikey,
            "X-RapidAPI-Host": "openai80.p.rapidapi.com"
        }
