import requests

url = "http://127.0.0.1:5000/analyze"

data = {
    "code": """
def test():
    for i in range(5):
        print(i)
"""
}

response = requests.post(url, json=data)
print(response.json())
import requests

url = "http://127.0.0.1:5000/analyze"

data = {
    "code": """
def test():
    for i in range(5):
        print(i)
"""
}

response = requests.post(url, json=data)
print(response.json())
