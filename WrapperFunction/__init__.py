import fastapi
import requests
from pydantic import BaseModel
from tldextract import tldextract

# sets a user agent header to mimic a real browser
UA_header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

# requires post body with a single attribute, url as a string
class URL(BaseModel):
    url: str

# starts the fastapi app
app = fastapi.FastAPI()

# route for api
# expects a get call with json post body of {"url":"{url}"}
@app.get("/fetchfavicon/", status_code=200)
async def fetch_favicon(url: URL, response: fastapi.Response):
    favicon_url = prepare_domain(url)

    try:
        return retrieve_favicon(favicon_url, response)

    # catch invalid server errors that would otherwise crash
    except (requests.exceptions.InvalidURL, requests.exceptions.SSLError):
        return error_response(response, url)

# helper functions
def retrieve_favicon(url: str, response: fastapi.Response) -> fastapi.Response:
    fav = requests.get(url, headers=UA_header, allow_redirects=True)

    if fav.status_code == 200:
        return fastapi.Response(content=fav.content, media_type="image/png") 
    # catch non-200 response errors
    else:
        return error_response(url, response)

def prepare_domain(url: URL) -> str:
    extracted = tldextract.extract(url.url)

    if extracted.subdomain != '':
        domain = extracted.subdomain + "." + extracted.domain + "." + extracted.suffix
    else:
        domain = extracted.domain + "." + extracted.suffix
    
    favicon_url = f"https://{domain}/favicon.ico"
    return favicon_url

def error_response(url:URL, response: fastapi.Response, ):
    response.status_code = 404
    error_response = {"Error": f"Could not locate favicon at {url}."} 
    return error_response