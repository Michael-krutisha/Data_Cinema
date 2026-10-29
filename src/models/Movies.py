from dataclasses import dataclass

@dataclass
class Movie:
    movie_id: int      
    title: str         
    genre: str          
    duration: int       
    age_rating: str     