import requests

url = "http://127.0.0.1:8000/analyze_scene"
data = {"description": "A high-speed car chase through city streets"}

response = requests.post(url, json=data)
print(response.json())
