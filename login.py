from pymongo import MongoClient

import secrets

class Connect(object):
    #this user only has find perms on books collection
    @staticmethod
    def reader_connection():
        return MongoClient(secrets.reader)
    #this user only has find, insert, update perms on books collection
    @staticmethod
    def writer_connection():
        return MongoClient(secrets.writer)
