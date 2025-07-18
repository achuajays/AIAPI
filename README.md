# FastAPI Multi-Service API

A comprehensive FastAPI application that provides multiple services including image generation, movie search, image search, and AI-powered query processing.

## 🚀 Features

- **Image Generation**: Generate images using AI models via Nebius API
- **Movie Search**: Search for movies and get recommendations using OMDb API
- **Image Search**: Search for images using Google Serper API
- **AI Query Processing**: Process queries using Groq LLM models
- **CORS Support**: Fully configured for cross-origin requests
- **Async Operations**: Optimized with async/await for better performance

## 📋 Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip or pipenv

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```env
NEBIUS_API_KEY=your_nebius_api_key
OMDB_API_KEY=your_omdb_api_key
SERPER_API_KEY=your_serper_api_key
GROQ_API_KEY=your_groq_api_key
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEBIUS_API_KEY` | API key for Nebius AI image generation | Yes |
| `OMDB_API_KEY` | API key for OMDb movie database | Yes |
| `SERPER_API_KEY` | API key for Google Serper image search | Yes |
| `GROQ_API_KEY` | API key for Groq LLM services | Yes |

## 🔗 API Endpoints

### Root Endpoint
- **GET** `/` - Welcome message

### Image Generation (`/image-gen`)
- **POST** `/image-gen/generate-image` - Generate images using AI

### Movie Services (`/omdb`)
- **POST** `/omdb/movie` - Get detailed movie information
- **POST** `/omdb/recommendations` - Get movie recommendations

### Image Search (`/image-search`)
- **GET** `/image-search/` - Welcome message
- **POST** `/image-search/search` - Search for movie posters

### Query Processing (`/query`)
- **POST** `/query/` - Process AI queries
- **GET** `/query/health` - Health check endpoint

## 📝 Usage Examples

### Image Generation

```bash
curl -X POST "http://localhost:8000/image-gen/generate-image" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains"
  }'
```

**Response:**
```json
{
  "image_b64": "base64_encoded_image_data"
}
```

### Movie Information

```bash
curl -X POST "http://localhost:8000/omdb/movie" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Matrix"
  }'
```

**Response:**
```json
{
  "title": "The Matrix",
  "year": "1999",
  "imdbRating": "8.7",
  "genre": "Action, Sci-Fi",
  "actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
  "plot": "A computer programmer is led to fight an underground war...",
  "poster": "https://example.com/poster.jpg"
}
```

### Movie Recommendations

```bash
curl -X POST "http://localhost:8000/omdb/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Matrix"
  }'
```

**Response:**
```json
[
  {
    "title": "The Matrix Reloaded",
    "year": "2003",
    "imdbRating": "7.2",
    "genre": "Action, Sci-Fi",
    "actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
    "plot": "Neo and his allies race against time...",
    "poster": "https://example.com/poster2.jpg"
  }
]
```

### Image Search

```bash
curl -X POST "http://localhost:8000/image-search/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "The Matrix"
  }'
```

**Response:**
```json
{
  "data": {
    "image_url": "https://example.com/matrix-poster.jpg"
  }
}
```

### AI Query Processing

```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is artificial intelligence?",
    "model": "meta-llama/llama-4-scout-17b-16e-instruct",
    "temperature": 0.7,
    "max_tokens": 1024
  }'
```

**Response:**
```json
{
  "answer": "Artificial intelligence (AI) is a branch of computer science..."
}
```

## 🚀 Deployment

### Vercel Deployment

This project is configured for Vercel deployment using the included `vercel.json` file.

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard or via CLI:
```bash
vercel env add NEBIUS_API_KEY
vercel env add OMDB_API_KEY
vercel env add SERPER_API_KEY
vercel env add GROQ_API_KEY
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fastapi-app .
docker run -p 8000:8000 --env-file .env fastapi-app
```

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`

## 🧪 Testing

### Health Check

```bash
curl -X GET "http://localhost:8000/query/health"
```

### Root Endpoint

```bash
curl -X GET "http://localhost:8000/"
```

## 🔧 Configuration

### CORS Settings

The application is configured to allow all origins, methods, and headers. For production, consider restricting these:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Model Configuration

The default AI model is `meta-llama/llama-4-scout-17b-16e-instruct`. You can specify different models in your requests:

- `meta-llama/llama-4-scout-17b-16e-instruct`
- Other Groq-supported models

## 🛡️ Error Handling

The API provides comprehensive error handling:

- **400**: Bad Request (missing API keys, invalid input)
- **404**: Not Found (movie not found, etc.)
- **500**: Internal Server Error (API failures, processing errors)

## 🔄 Rate Limiting

Be aware of rate limits for external APIs:

- **OMDb API**: 1,000 requests per day (free tier)
- **Nebius API**: Check your plan limits
- **Serper API**: Check your plan limits
- **Groq API**: Check your plan limits

## 📞 Support

For issues and questions:

1. Check the [API documentation](http://localhost:8000/docs)
2. Review error messages and logs
3. Ensure all environment variables are correctly set
4. Verify API key validity and quotas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [OMDb API](http://www.omdbapi.com/) for movie data
- [Nebius](https://nebius.com/) for AI image generation
- [Groq](https://groq.com/) for LLM services
- [Serper](https://serper.dev/) for image search capabilities
