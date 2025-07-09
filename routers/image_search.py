from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import Optional

router = APIRouter()

class PosterSearchRequest(BaseModel):
    query: str

class PosterSearchResponse(BaseModel):
    data: dict

# Get OMDb API key from environment variable
api_key = "e9416d5f"

@router.get("/")
def read_root():
    return {"message": "Welcome to the OMDb Poster Search API"}

@router.post("/search", response_model=PosterSearchResponse)
async def search_images(request: PosterSearchRequest):
    """
    Search for a movie poster using OMDb API
    """
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="API key is required. Please set OMDB_API_KEY environment variable"
        )

    url = "http://www.omdbapi.com/"
    print(request.query)
    params = {
        "apikey": api_key,
        "t": request.query.strip()
    }

    try:
        response = requests.get(url, params=params)
        print(response)

        response.raise_for_status()
        print(response)
        movie_data = response.json()
        print(movie_data)

        if movie_data.get("Response") != "True":
            raise HTTPException(
                status_code=404,
                detail=movie_data.get("Error", "Movie not found")
            )

        poster_url = movie_data.get("Poster", None)
        if not poster_url or poster_url == "N/A":
            poster_url = None

        return PosterSearchResponse(data={"image_url": poster_url})

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to OMDb API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
