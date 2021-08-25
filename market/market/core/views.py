from flask import render_template,request,Blueprint
from market.models import Item

core = Blueprint('core',__name__)

@core.route('/')
def info():
    return render_template('info.html')