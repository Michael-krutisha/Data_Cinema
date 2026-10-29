from dataclasses import dataclass

@dataclass
class Ticket:
    ticket_id: int       
    session_id: int      
    user_id: int        
    ticket_price: int    
    row_number: int      
    seat_number: int     
    payment_status: bool 
    
    movie_title: str | None = None  
    date_time: str | None = None