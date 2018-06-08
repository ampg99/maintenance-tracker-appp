from flask_jwt_extended import get_jwt_identity, jwt_required

from ..model.db import MainDB
from flask_redis import Redis

redis_store = Redis()
db = MainDB()


@jwt_required
def get_current_user():
    return db.users.query_by_field("username", get_jwt_identity())
