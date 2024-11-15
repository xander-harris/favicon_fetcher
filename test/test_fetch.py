import requests

url = "https://favicon-fetcher.azurewebsites.net/fetchfavicon/"
body = {"url": "https://poncho.com"}

response = requests.get(url, json=body)

open('test.png', 'wb').write(response.content)