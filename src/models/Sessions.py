from dataclasses import dataclass

@dataclass
class Session:
    session_id: int     
    movie_id: int       
    hall_id: int        
    date_time: str     
    
    movie_title: str | None = None  
    hall_name: str | None = None