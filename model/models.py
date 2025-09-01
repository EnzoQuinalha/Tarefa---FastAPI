from typing import Optional
from pydantic import BaseModel

class Index(BaseModel):
    searchTerm: str
    count: Optional[int] = 1
    poster_url: str
    movie_id: int

