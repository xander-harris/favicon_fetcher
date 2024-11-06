import requests

url = "http://127.0.0.1:8000/fetchfavicon/"
body = {"url": "data"}
response = requests.get(url, json=body)

open('test.png', 'wb').write(response.content)