from email.policy import default
from sre_constants import SUCCESS
import uuid
import hashlib

from sanic import Blueprint
from sanic.response import json

from app.utils.jwt_utils import generate_jwt
from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiInternalError
from app.models.user import user_json_schema, User
from app.hooks.error import ApiInternalError


users_bp = Blueprint('users_blueprint', url_prefix='/users')

_db = MongoDB()

# r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
@users_bp.route('/', methods = {'GET'})
async def get_all_user(request):
    # async with request.app.ctx.redis as r:
    #     users = await get_cache(r, CacheConstants.all_users)
    #     if users is None:
    #         filter = {}
    #         user_objs = _db.get_users()
    #         users = [user.to_dict() for user in user_objs]
    #         await set_cache(r, CacheConstants.all_users, users)
    user_objs = _db.get_users()
    users = [user.to_dict() for user in user_objs]        
    number_of_users = len(users)
    return json({
        'n_users': number_of_users,
        'users': users
    })
    
@users_bp.route('/register', methods={'POST'})
@validate_with_jsonschema(user_json_schema)  # To validate request body
async def register_user(request):
    user_name = request.json["username"]
    check_name = _db._users_col.find_one({"username":user_name})
    if check_name:
        return json({
        'status': "Username existed"
    }) 
    user_id = str(uuid.uuid4())
    user_password = str(hashlib.md5(request.json["password"].encode()).hexdigest())
    user = User(user_id,user_name,user_password)
    register =  _db.register_user(user)
    if not user:
        raise ApiInternalError('Fail to create user')
    # async with request.app.ctx.redis as r:
    #     set_cache(r, CacheConstants.all_users,register)
    return json({
        'status': "User create success"
    })
    
@users_bp.route('/login', methods={'PUT'})
@validate_with_jsonschema(user_json_schema)  # To validate request body
async def register_user(request):
    user_name = request.json["username"]
    user_password = str(hashlib.md5(request.json["password"].encode()).hexdigest())
    account = _db._users_col.find_one({"username" : user_name, "password" : user_password})
    if not account :
        return json({
        'status': "Wrong information"
    })
    _db._users_col.find_one_and_update({"username" : user_name},{"$set" : {"login" : True}})
    
    token_jwt = generate_jwt(user_name)
    
    return json({
        'status': "Login success",
        'token' : token_jwt
    })

    

    


