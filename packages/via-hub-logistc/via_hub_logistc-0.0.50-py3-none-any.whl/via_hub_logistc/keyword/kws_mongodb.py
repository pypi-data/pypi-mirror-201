import pymongo

from robot.api.logger import info
from robot.api.deco import keyword
from robot.api import Error


class ViaMongo():
    ### Return conncection with mongoDB ###
    @keyword(name="Mongo Connect To Database")
    def mongo_connect_to_database(self, strConnction):
        try:
            return pymongo.MongoClient(f"mongodb://{strConnction}/")
        except Exception as e:
            raise Error(e)

    ### Returns a disconnection with the server ###
    @keyword(name="Mongo Disconnect To Database")
    def mongo_disconnect_to_database(self, client):
        try:
            client.close()
            info("Connection has closed sucess")
        except Exception as e:
            raise Error(e)

    ### Returns one json or list the json result ###
    @keyword(name="Mongo Find All")
    def mongo_find_all(self, client, baseName, collectionName):
        try:
            lstItems = []

            dataBase = client[baseName]

            collection = dataBase[collectionName]

            result = collection.find()

            for item in result:
                lstItems.append(item)

            return lstItems
        except Exception as e:
            raise Error(e)

    ### Returns one json or list the json result by parameter ###
    @keyword(name="Mongo Find By Parameter")
    def mongo_find_by_parameter(self, client, baseName, collectionName, filter):
        try:
            dataBase = client[baseName]

            collection = dataBase[collectionName]

            return collection.find(filter)
        except Exception as e:
            raise Error(e)
