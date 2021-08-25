from flask import render_template,request,Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def info():
    return render_template('info.html')