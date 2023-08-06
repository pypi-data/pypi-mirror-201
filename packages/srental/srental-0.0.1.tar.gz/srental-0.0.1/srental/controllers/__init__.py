from flask import Blueprint

app = Blueprint('spaceship', __name__)

from . import spaceship
