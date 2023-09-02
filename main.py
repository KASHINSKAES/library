from fastapi import FastAPI
from config import *
from schemas import *
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [""]
import psycopg2
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
con = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD, host=DB_HOST )
cursor = con.cursor()

@app.get('/get_all_books')
def get_all_books():
    cursor.execute("SELECT * FROM books")
    fet = cursor.fetchall()
    output_List = []
    for books in fet:
        output_List.append({'id':books[0],'naimenovanie':books[1],'avtor':books[2],'zalogovai_ctoimost':books[3], 'ctoimost_prokata':books[4],'zhanr':books[5]})
    return output_List

@app.get('/get_all_issued_books')
def get_all_books():
    cursor.execute("SELECT b.naimenovanie, r.familia, r.imia, ib.data_vidochi,ib.data_vozvrata,CASE WHEN (ib.data_vozvrata-ib.data_vidochi)<7 then 'good' else 'bad' end FROM issued_books ib JOIN books b ON ib.books_id=b.id JOIN readers r ON ib.readers_id=r.id WHERE ib.data_vozvrata is not null")
    fet = cursor.fetchall()
    output_List = []
    for books in fet:
        output_List.append({'naimenovanie':books[0],'familia':books[1],'imia':books[2], 'data_vidochi':books[3],'data_vozvrata':books[4],'statys':books[5]})
    return output_List

@app.get('/returned_or_not')
def returned_or_not():
    cursor.execute("SELECT b.naimenovanie, r.familia, r.imia, ib.data_vidochi,ib.data_vozvrata,CASE WHEN ib.data_vozvrata is not null then 'returned' else 'did not return' end FROM issued_books ib JOIN books b ON ib.books_id=b.id JOIN readers r ON ib.readers_id=r.id")
    fet = cursor.fetchall()
    output_List = []
    for books in fet:
        output_List.append({'naimenovanie':books[0],'familia':books[1],'imia':books[2], 'data_vidochi':books[3],'data_vozvrata':books[4],'statys':books[5]})
    return output_List

@app.post('/create_readers',status_code=200)
def create_readers(item: Readers):
    cursor.execute(f"""INSERT INTO public.readers(familia, imia, otchestvo, gorod, ylica, dom, telefon) VALUES ('{item.familia}','{item.imia}','{item.otchestvo}','{item.gorod}','{item.ylica}','{item.dom}','{item.telefon}')""")
    con.commit()
    return "good"

@app.post('/create_books',status_code=200)
def create_books(item: Books):
    cursor.execute(f"""INSERT INTO public.books(naimenovanie, avtor, zalogovai_ctoimost, ctoimost_prokata, zhanr)
	VALUES ('{item.naimenovanie}','{item.avtor}','{item.zalogovai_ctoimost}','{item.ctoimost_prokata}','{item.zhanr}')""")
    con.commit()
    return "good"

@app.put("/Change_info")
def Change_info(item: Issued_books):
    cursor.execute(f"UPDATE public.issued_books SET data_vozvrata='{item.data_vozvrata}' WHERE books_id='{item.books_id}' AND readers_id='{item.readers_id}'")
    con.commit()
    return "good"

@app.post('/create_issued_books',status_code=200)
def create_issued_books(item: Issued_books , book: Books , reader: Readers):
    cursor.execute(f"""INSERT INTO public.issued_books( books_id, readers_id, data_vidochi, data_vozvrata) SELECT b.id, r.id,'{item.data_vidochi}' ,'{item.data_vozvrata}' FROM books b, readers r
	WHERE r.familia='{reader.familia}' AND b.naimenovanie='{book.naimenovanie}'""")
    con.commit()
    return "good"

