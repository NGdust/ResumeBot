import pymongo


class DB:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.db = pymongo.MongoClient(self.host, self.port).teledaemon
        self.db_tokens = self.db.tokens
        self.db = self.db.users

    def migrate(self):
        if self.db.count_documents({}) == 0:
            self.db.insert_one({"chat_id": None, "status": None, "level": None, "type": None})