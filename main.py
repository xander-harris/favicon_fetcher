from fastapi import FastAPI, Response
from pydantic import BaseModel
from tldextract import tldextract
import requests

UA_header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

class URL(BaseModel):
    url: str

app = FastAPI()

@app.get("/fetchfavicon/", status_code=200)
async def fetch_favicon(url: URL, response: Response):
    extracted = tldextract.extract(url.url)

    if extracted.subdomain != '':
        domain = extracted.subdomain + "." + extracted.domain + "." + extracted.suffix
    else:
        domain = extracted.domain + "." + extracted.suffix
    
    favicon_url = f"https://{domain}/favicon.ico"

    try:
        fav = requests.get(favicon_url, headers=UA_header, allow_redirects=True)
        if fav.status_code == 200:
            return Response(content=fav.content, media_type="image/png") 
        else:
            return error_response(response, url)

    except (requests.exceptions.InvalidURL, requests.exceptions.SSLError):
        return error_response(response, url)
         
def error_response(response: Response, url:URL):
    response.status_code = 404
    error_response = {"Error": f"Could not locate favicon for {url.url}."} 
    return error_response