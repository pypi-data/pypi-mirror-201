import pymongo


class ConnectionDefinition():
    def __init__(self, mongo_url:str):
        self.mongo_url = mongo_url
        client = self.get_client()        
        self.db_name = client.list_database_names()[0]

    def get_client(self):
        return pymongo.MongoClient(self.mongo_url)

    def get_database(self):
        return self.get_client()[self.db_name]

