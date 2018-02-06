# 导入admin蓝本
from . import admin
# 导入
from flask import render_template

# 路由修饰器，命名规则为 @蓝本名.route('/url地址')
@admin.route('/login')
# 对应路由的视图函数，这个函数进行相应的程序处理后，返回响应到客户端(return 响应)，
# 在这里响应为 templates/admin 文件夹下的 login.html 文件
def login():
    return render_template('admin/login.html')