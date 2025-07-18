import os
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/image-gen",
    tags=["image-gen"]
)

class PromptRequest(BaseModel):
    prompt: str

@router.post("/generate-image")
def generate_image(request: PromptRequest):
    api_key = os.getenv("NEBIUS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found.")
    client = OpenAI(
        base_url="https://api.studio.nebius.com/v1/",
        api_key=api_key
    )
    try:
        response = client.images.generate(
            model="black-forest-labs/flux-schnell",
            response_format="b64_json",
            extra_body={
                "response_extension": "png",
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 4,
                "negative_prompt": "",
                "seed": -1,
                "loras": None
            },
            prompt=request.prompt
        )
        return {"image_b64": response.data[0].b64_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))