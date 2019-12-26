from flask import Flask, session
import os, cloudinary as _cloud, cloudinary.uploader
from flask_bcrypt import Bcrypt

boop = Flask(__name__)

flask_bcrypt = Bcrypt()

boop.config["SECRET_KEY"] = os.urandom(24)

_cloud.config(
  cloud_name = "fmscrns",
  api_key = "231339544622852",  
  api_secret = "cR3RImpJd8njjhS8-zO5GDRacO4"  
)

@boop.after_request
def add_header(response):
    if "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "no-store"
        
    return response

from app import routes