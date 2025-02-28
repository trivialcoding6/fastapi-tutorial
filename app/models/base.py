from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    
    class Config:
        arbitrary_types_allowed = True