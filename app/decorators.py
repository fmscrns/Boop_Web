from flask import session, redirect, url_for
from functools import wraps

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