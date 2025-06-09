from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
from metabase_api.generate_card.generate_card import handle_user_request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class URLRequest(BaseModel):
    body: str

@app.post("/fetch-url")
async def fetch_url(request: URLRequest):
    try:
        request_body = request.body
        if not request_body:
            raise HTTPException(status_code=400, detail="Request body is empty")
        
        response = handle_user_request(request_body)

        if response:
            response_str = "\n".join(response)
            print(f"Response: {response_str}")
            return {"status": "success", "content": f' {response_str}'}
        else:
            raise HTTPException(status_code=500, detail="No content returned from server")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
