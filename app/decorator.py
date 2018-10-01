from functools import wraps
from .users.models import User
from flask_jwt_extended import get_jwt_identity

def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = get_jwt_identity()
        user =User.fetch_user_by_id(current_user)
        print(user)
        admin =user['is_admin'] == True
        if admin:
            return f(*args, **kwargs)
        else:
            return {'message':'You can not acces this end point'},401
    return decorated