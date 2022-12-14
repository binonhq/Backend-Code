from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.models.book import Book
from app.models.user import User
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            # connection_url = f'mongodb://localhost:27017/'
            connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'

        self.connection_url = connection_url.split('@')[-1]
        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]
        self._books_col = self.db[MongoCollections.books]
        self._users_col = self.db[MongoCollections.users]

    def get_all_books(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._books_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))   
            return data
        except Exception as ex:
            logger.exception(ex)
        return []
    
    def get_book(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            data = self._books_col.find_one(filter_, projection=projection)
            return data
        except Exception as ex:
            logger.exception(ex)
        return None


    def add_book(self, book: Book):
        try:
            inserted_doc = self._books_col.insert_one(book.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None
    
    def update_book(self, filter_=None, updateFilter_=None):
        try:
            if not filter_:
                filter_={}
            update_doc = self._books_col.find_one_and_update(filter_, updateFilter_)
            return update_doc
        except Exception as ex:
            logger.exception(ex)
        return None
            
    
    def delete_book(self, filter_: None):
        try:
            if not filter_:
                return None
            delete_doc = self._books_col.delete_one(filter_)
            return delete_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    def register_user(self, user: User):
        try:
            inserted_user = self._users_col.insert_one(user.to_dict())
            return inserted_user
        except Exception as ex:
            logger.exception(ex)
        return None
    
    def get_users(self, filter_=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._users_col.find(filter_)
            data = []
            for doc in cursor:
                data.append(User().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []
    
        

    # TODO: write functions CRUD with books
