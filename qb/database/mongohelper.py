__author__ = 'gaurav'

from qb import client

class mongohelper():
    @staticmethod
    def insertindatabse(database, collectionname, object):
        db = client[database]
        collections = db[collectionname]
        collections.insert(object,manipulate=False)


