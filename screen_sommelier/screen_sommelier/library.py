from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from .auth import login_required
from .db import get_db

bp = Blueprint('library', __name__, url_prefix = '/library')

@bp.route('/')
def library_home():
    return render_template("library/library_base.html")