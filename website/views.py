from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User, Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)
