from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_db, MovieModel
from src.schemas import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter(prefix="/movies")


@router.get("/", response_model=MovieListResponseSchema)
async def get_all_movies(db: AsyncSession = Depends(get_db),
                         page: int = Query(1, ge=1),
                         per_page: int = Query(10, ge=1, le=20)):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")
    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page

    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()
    movies_pydantic = [MovieDetailResponseSchema.model_validate(movie) for movie in movies]

    base_url = "/theater/movies"
    prev_page = f"{base_url}/?page={page - 1}&per_page={per_page}" if page > 1 else ""
    next_page = f"{base_url}/?page={page + 1}&per_page={per_page}" if page < total_pages else ""

    return MovieListResponseSchema(
        movies=movies_pydantic,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{id}/", response_model=MovieDetailResponseSchema)
async def get_one_movie(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.model_validate(movie)
