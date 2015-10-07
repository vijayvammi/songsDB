from flask import Flask
app = Flask(__name__)

from app import database
from app import views
