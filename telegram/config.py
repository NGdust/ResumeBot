from database import DB

class Config:
    BOT_TOKEN = '1349245843:AAE7ffXUwG7iPWAvui3IRhagNrFqhZ7JGVA'
    HOST = 'http://127.0.0.1:8000/api/v1/user/'

    db = DB("localhost", 27017)
    db.migrate()
    db = db.db

    E_START = 'e0'
    C_START = 'c0'