import requests

url = "http://127.0.0.1:8000/upload-audio/"
file_path = "sample.mp3"

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print(response.json())
url = "http://127.0.0.1:8000/submit-text/"
data = {
    "text": "This is a sample text.",
    "additional_info": "Some optional information"
}

response = requests.post(url, json=data)
print(response.json())