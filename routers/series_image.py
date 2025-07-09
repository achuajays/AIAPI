from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import json
import os
from typing import Optional

router = APIRouter()

class ImageSearchRequest(BaseModel):
    query: str
    
class ImageSearchResponse(BaseModel):
    data: dict 

# Get API key from environment variable
api_key = os.getenv("SERPER_API_KEY")

@router.get("/")
def read_root():
    return {"message": "Welcome to the Image Search API"}

@router.post("/search", response_model=ImageSearchResponse)
async def search_images(search_request: ImageSearchRequest):
    """
    Search for images using Google Serper API
    """
    if not api_key:
        raise HTTPException(
            status_code=400, 
            detail="API key is required. Please set SERPER_API_KEY environment variable"
        )
    
    url = "https://google.serper.dev/images"
    
    payload = json.dumps({
        "q": search_request.query
    })
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        
        res = response.json()
        print("Full response:", res)
        
        # Check if the response has the expected structure
        if "images" not in res:
            raise HTTPException(
                status_code=500,
                detail="Unexpected response format from Serper API"
            )
        
        images = res["images"]
        print("Images found:", len(images))
        
        # Get first image URL if available
        first_image_url = None
        if images and len(images) > 0:
            first_image_url = images[0].get("imageUrl")
            print("First image URL:", first_image_url)

        return ImageSearchResponse(
            data={"image_url": first_image_url}
        )
        
    except requests.exceptions.RequestException as e:
        # Handle case where response might not be defined
        status_code = 500
        try:
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
        except:
            pass
            
        raise HTTPException(
            status_code=status_code,
            detail=f"Error from Serper API: {str(e)}"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid JSON response from Serper API"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )