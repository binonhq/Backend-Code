from email.policy import default
from sre_constants import SUCCESS
import uuid

from sanic import Blueprint
from sanic.response import json

from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.auth import protected
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiBadRequest, ApiInternalError, ApiNotFound, ApiUnauthorized
from app.models.book import update_book_json_schema, create_book_json_schema, Book
from app.models.user import User
from app.hooks.error import ApiInternalError


books_bp = Blueprint('books_blueprint', url_prefix='/books')
users_bp = Blueprint('books_blueprint', url_prefix='/users')

_db = MongoDB()

# r = redis.StrictRedis(host='localhost', port=6379, db=0)


@books_bp.route('/', methods = {'GET'})
async def get_all_book(request):
    # TODO: use cache to optimize api
     
    async with request.app.ctx.redis as r:
        books = await get_cache(r, CacheConstants.all_books)
        if books is None:
            filter = {}
            book_objs = _db.get_all_books()
            books = [book.to_dict() for book in book_objs]
            await set_cache(r, CacheConstants.all_books, books)
    # book_objs = _db.get_books()
    # books = [book.to_dict() for book in book_objs]        
    number_of_books = len(books)
    return json({
        'n_books': number_of_books,
        'books': books
    })
    
@books_bp.route('/<book_id>', methods = {'GET'})
async def get_book(request, book_id):
    filter = {"_id" : book_id}
    book = _db.get_book(filter)
    if not book: 
        raise ApiBadRequest("Not found book")
    return json({
        'Book': book
    })



@books_bp.route('/', methods={'POST'})
@protected  # TODO: Authenticate
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username=None):
    body = request.json
    book_id = str(uuid.uuid4())
    book = Book(book_id).from_dict(body)
    book.owner = username
    inserted = _db.add_book(book)
    if not inserted:
        raise ApiInternalError('Fail to create book')
    
    async with request.app.ctx.redis as r:
        book_objs = _db.get_all_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)
    
    return json({'status': 'success'})

@books_bp.route('/<book_id>', methods={'PUT'})
@protected  # TODO: Authenticate
@validate_with_jsonschema(update_book_json_schema)  # To validate request body

async def update_book(request, book_id, username=None):
    filter_find = {"_id": book_id}
    book = _db.get_book(filter_find)
    if not book : 
        raise ApiNotFound('Dont exist book')
    if book['owner'] != username:
        raise ApiUnauthorized("Dont have permission to update this book")
    
    filter_update = request.json
    update = _db.update_book(filter_find,{"$set":filter_update})
    
    if not update:
        raise ApiInternalError('Fail to update book')
    
    return json({
        'status': "update success"
    })
    
@books_bp.route('/<book_id>', methods={'DELETE'})
@protected  # TODO: Authenticate
async def delete_book(request, book_id, username=None):
    filter_find = {"_id": book_id}
    book = _db.get_book(filter_find)
    if not book : 
        raise ApiNotFound('Dont exist book')
    if book['owner'] != username:
        raise ApiUnauthorized('Dont have permission to delete this book')
    delete = _db.delete_book(filter_find)
    if not delete:
        raise ApiInternalError('Fail to delete book')
    async with request.app.ctx.redis as r:
        book_objs = _db.get_all_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)

    return json({
        'status': "delete success"
    })
    
    

    

    


