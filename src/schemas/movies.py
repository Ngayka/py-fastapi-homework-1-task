from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class MovieBase(BaseModel):
    name: str
    date: date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    model_config = {
        "from_attributes": True
    }


class MovieListResponseSchema(MovieBase):
    pass


class MovieDetailResponseSchema(MovieListResponseSchema):
    id: int


class PaginationMoviesResponse(BaseModel):
    movies: List[MovieBase]
    prev_page: int | None
    next_page: int | None
    total_pages: int
    total_items: int
