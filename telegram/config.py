from database import DB

class Config:
    BOT_TOKEN = '1349245843:AAE7ffXUwG7iPWAvui3IRhagNrFqhZ7JGVA'
    HOST = 'http://127.0.0.1:8000/'
    USER_API = 'api/v1/user/'
    DATA_API = 'api/v1/data/'

    db = DB("localhost", 27017)
    db.migrate()
    db = db.db
