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
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "openai80.p.rapidapi.com"
        }

class ImageGenerator:
    def __init__(self, prompt, image_size, api_key):
        self.payload = {    
            "prompt": prompt,
            "n": 2,
            "size": image_size   
        }
        self.headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "openai80.p.rapidapi.com"
        }
