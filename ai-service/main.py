from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .emotion import detect_emotions
from .toxicity_detector import detector

app = FastAPI()

# origins = ["http://localhost:8000", "http://localhost"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Comment(BaseModel):
    id: int
    comment: str


class CommentOut(Comment):
    confidence: float
    is_toxic: bool | None = False


@app.get("/health")
def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "healthy"}


@app.get("/")
async def index():
    return {"msg": "fastapi service"}


@app.post("/predict-toxicity")
async def predict_toxicity(comments: list[Comment]):
    results = []
    for comment in comments:
        is_toxic, final_score, _ = detector.detect_toxicity(comment.comment)
        results.append(
            CommentOut(
                id=comment.id,
                comment=comment.comment,
                confidence=final_score,
                is_toxic=bool(is_toxic),
            )
        )

    return {"results": results}


class EmotionIn(BaseModel):
    id: int
    content: str


class EmotionOut(EmotionIn):
    emotion: str
    score: float


@app.post("/emotions")
async def get_emotions(contents: list[EmotionIn]):
    if len(contents) > 0:
        return {"emotions": detect_emotions(contents)}
    return {"emotions": []}
