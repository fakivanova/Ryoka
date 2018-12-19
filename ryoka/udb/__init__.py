from flask import Blueprint

udb = Blueprint('udb', __name__)

from . import views
