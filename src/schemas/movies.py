from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str

    model_config = {
        "from_attributes": True
    }


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: str
    next_page: str
    next_page: str
    total_pages: int
    total_items: int
