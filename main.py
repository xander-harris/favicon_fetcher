from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from tldextract import tldextract
import requests

UA_header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

class URL(BaseModel):
    url: str

app = FastAPI()

@app.get("/fetchfavicon/")
async def send_file(url: URL):
    filepath = fetch_favicon(url.url) 
    return FileResponse(filepath)

def fetch_favicon(url=URL):
    extracted = tldextract.extract(url)
    domain = extracted.subdomain + "." + extracted.domain + "." + extracted.suffix

    favicon_url = f"https://{domain}/favicon.ico"
    response = requests.get(favicon_url, headers=UA_header)

    filepath = f'./assets/{extracted.domain}.png'
    
    open(filepath, 'wb').write(response.content)

    return filepath

# to debug ##
import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)