from flask import session, redirect, url_for, abort
from functools import wraps
from app.services import User

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "booped_in" in session:
            return f(*args, **kwargs)

        else:
            return redirect(url_for("login"))
    
    return wrap

def inaccesible_if_authenticated(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "booped_in" in session:
            return redirect(url_for("home"))
        
        else:
            return f(*args, **kwargs)

    return wrap

def access_to_pet_owners_only(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = User.get_current_user()

        owner_list = User.get_pet_owners(kwargs["public_id"])["data"]

        for user in owner_list:
            if current_user["username"] == user["username"]:
                return f(*args, **kwargs)

        abort(405)

    return wrap