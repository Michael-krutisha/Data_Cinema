from dataclasses import dataclass # автоматически собирает внутренность

@dataclass
class Session:
    session_id: int     
    movie_id: int       
    hall_id: int        
    date_time: str     
    
    movie_title: str | None = None #чтобы можно было указать цифру, после выдаст название или сам зал который выбрали 
    hall_name: str | None = None