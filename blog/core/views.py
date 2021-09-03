from flask import render_template,request,Blueprint
from blog.models import BlogPost

core = Blueprint('core',__name__)

@core.route('/')
def info():
    return render_template('info.html')

@core.route('/blog_posts')
def info():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html')