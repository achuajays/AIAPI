from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import httpx
import asyncio

router = APIRouter()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"

class MovieRequest(BaseModel):
    title: str

class RecommendationResponse(BaseModel):
    title: str
    year: str
    imdbRating: str
    genre: str
    actors: str
    plot: str
    poster: Optional[str]

async def get_full_movie_data_async(imdb_id: str, client: httpx.AsyncClient) -> dict:
    params = {"apikey": OMDB_API_KEY, "i": imdb_id}
    response = await client.get(BASE_URL, params=params)
    return response.json()

async def search_movies_by_keyword_async(keyword: str, client: httpx.AsyncClient) -> List[dict]:
    params = {"apikey": OMDB_API_KEY, "s": keyword, "type": "movie"}
    response = await client.get(BASE_URL, params=params)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("Search", [])[:3]  # limit to top 3
    return []

def get_movie(title: str) -> dict:
    params = {"apikey": OMDB_API_KEY, "t": title}
    response = httpx.get(BASE_URL, params=params)
    data = response.json()
    return data if data.get("Response") == "True" else None

async def recommend_movies_async(base_movie: dict) -> List[dict]:
    keywords = base_movie.get("Genre", "").split(", ") + base_movie.get("Actors", "").split(", ")[:2]
    seen_ids = set()
    recommendations = []

    async with httpx.AsyncClient() as client:
        search_tasks = [search_movies_by_keyword_async(kw, client) for kw in keywords]
        search_results_lists = await asyncio.gather(*search_tasks)

        movie_tasks = []
        for results in search_results_lists:
            for movie in results:
                imdb_id = movie.get("imdbID")
                if imdb_id and imdb_id not in seen_ids and imdb_id != base_movie["imdbID"]:
                    seen_ids.add(imdb_id)
                    movie_tasks.append(get_full_movie_data_async(imdb_id, client))

        full_movies = await asyncio.gather(*movie_tasks)
        recommendations.extend([m for m in full_movies if m.get("Response") == "True"])

    return recommendations

@router.post("/movie", response_model=RecommendationResponse)
async def fetch_movie_info(request: MovieRequest):
    movie = get_movie(request.title)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return RecommendationResponse(
        title=movie.get("Title"),
        year=movie.get("Year"),
        imdbRating=movie.get("imdbRating"),
        genre=movie.get("Genre"),
        actors=movie.get("Actors"),
        plot=movie.get("Plot"),
        poster=movie.get("Poster")
    )

@router.post("/recommendations", response_model=List[RecommendationResponse])
async def recommend_similar_movies(request: MovieRequest):
    base_movie = get_movie(request.title)
    if not base_movie:
        raise HTTPException(status_code=404, detail="Base movie not found")

    recommendations = await recommend_movies_async(base_movie)

    return [
        RecommendationResponse(
            title=movie.get("Title"),
            year=movie.get("Year"),
            imdbRating=movie.get("imdbRating"),
            genre=movie.get("Genre"),
            actors=movie.get("Actors"),
            plot=movie.get("Plot"),
            poster=movie.get("Poster")
        )
        for movie in recommendations[:5]  # top 5
    ]
