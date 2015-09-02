from flask import Blueprint, Response, request, render_template
import json
import settings
import functions
routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html')