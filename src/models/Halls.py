from dataclasses import dataclass

@dataclass
class Hall:
    hall_id: int         
    name: str          
    rows_count: int     
    seats_per_row: int  