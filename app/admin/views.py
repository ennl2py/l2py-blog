# 导入admin蓝本
from . import admin
from flask import render_template

# 后台登录页
@admin.route('/login')
def login():
    return render_template('admin/login.html')

# 后台首页
@admin.route('/')
def index():
    return render_template('admin/index.html')

# 文章页面
@admin.route('/article')
def article():
    return render_template('admin/article.html')

# 文章分类页面
@admin.route('/category')
def category():
    return render_template('admin/category.html')

# 用户页面
@admin.route('/user')
def user():
    return render_template('admin/user.html')

# 文章评论页面
@admin.route('/article/<int:id>/comments')
def article_comments(id):
    return render_template('admin/comment.html', id=id)

# 文章添加页面
@admin.route('/add/article')
def add_article():
    return render_template('admin/editearticle.html')

