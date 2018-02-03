from . import admin
from flask import render_template

@admin.route('/login')
def login():
    return render_template('admin/login.html')