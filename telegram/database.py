import pymongo


class DB:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.db = pymongo.MongoClient(self.host, self.port).teledaemon
        self.db_tokens = self.db.tokens
        self.db = self.db.users