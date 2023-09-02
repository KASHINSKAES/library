from pydantic import BaseModel
import datetime

class Readers(BaseModel):
    familia:str
    imia:str
    otchestvo:str
    gorod:str
    ylica:str
    dom:str
    telefon:str

class Books(BaseModel):
    naimenovanie:str
    avtor:str
    zalogovai_ctoimost:int
    ctoimost_prokata:int
    zhanr:str

class Issued_books(BaseModel):
    books_id:int 
    readers_id:int 
    data_vidochi:datetime.date 
    data_vozvrata:datetime.date 