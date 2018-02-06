# 导入main蓝本
from . import main
from flask import render_template

# 路由修饰器，命名规则为 @蓝本名.route('/url地址')
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/article')
def article():
    return render_template('article.html')

@main.route('/test')
def test():
    return 'Hello,Word!'