import uuid
import hashlib

from sanic import Blueprint
from sanic.response import json
from app.decorators.auth import protected
from app.utils.jwt_utils import generate_jwt
from app.databases.mongodb import MongoDB
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiBadRequest, ApiInternalError
from app.models.user import user_json_schema, User
from app.hooks.error import ApiInternalError

users_bp = Blueprint('users_blueprint', url_prefix='/users')

_db = MongoDB()


# r = redis.StrictRedis(host='localhost', port=6379, db=0)

@users_bp.route('/', methods={'GET'})
async def get_all_user(request):
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
    check_name = _db._users_col.find_one({"username": user_name})
    if check_name:
        raise ApiBadRequest("Username existed")

    user_id = str(uuid.uuid4())
    user_password = str(hashlib.md5(request.json["password"].encode()).hexdigest())
    user = User(user_id, user_name, user_password)
    register = _db.register_user(user)
    if not user:
        raise ApiInternalError('Fail to create user')
    # async with request.app.ctx.redis as r:
    #     user_objs = _db.get_users()
    #     users = [user.to_dict() for user in user_objs]
    #     set_cache(r, CacheConstants.all_users,users)
    return json({
        'status': "User create success"
    })


@users_bp.route('/login', methods={'POST'})
@validate_with_jsonschema(user_json_schema)
async def login_user(request):
    user_name = request.json["username"]
    user_password = str(hashlib.md5(request.json["password"].encode()).hexdigest())
    account = _db._users_col.find_one({"username": user_name, "password": user_password})
    if not account:
        raise ApiBadRequest("Wrong information")

    token_jwt = generate_jwt(user_name).decode("utf-8")

    return json({
        'status': "Login success",
        'jwt_token': token_jwt
    })


@users_bp.route('/now', methods={'GET'})
@protected
async def now_user(request, username):
    return json({
        'now user': username
    })


@users_bp.route('/logout', methods={'GET'})
@protected
async def now_user(request, username):
    return json({
        'status': "logout success"
    })
