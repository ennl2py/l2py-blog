from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# 创建flask_extensions(即相应Flask扩展)的实例，创建后才可以调用类的方法
# 这里引用的所有扩展基本上都需要在后续 create_app() 工厂函数中进行初始化操作
db = SQLAlchemy()

# create_app()函数接收一个参数，即config.py文件里面所定义的config字典里面的key('development','production'和'default')
def create_app(config_name):
    # 创建Flask程序的实例，这个实例是Flask类的对象，Flask类只有一个必须指定的参数,即程序的主模块或者包的名字，一般使用__name__即可
    # Flask用这个参数决定程序的根目录，以便之后能找到相对于程序根目录的资源文件位置，当前的Flask程序实例为app
    app = Flask(__name__)

    # 程序实例创建后，需要加载程序定义配置项（即config.py文件里面所定义的诸如SECRET_KEY，DEBUG等配置项）
    # 程序配置项通过使用 app.config 配置对象提供的 from_object() 方法导入 config[key] 来完成
    app.config.from_object(config[config_name])

    # 这里因为在config.py中的Config基类里面定义了静态方法 init_app ，而不同环境的配置类都继承于该类
    # 本例中Config.init_app()方法为空函数，但是可能之后你需要在Production配置类中定义一定的方法
    # 定义之后要初始化，就需要调用config[config_name].init_app(app)
    config[config_name].init_app(app)

    # 然后开始进行相应Flask扩展的初始化操作
    db.init_app(app)

    # 注册前台蓝本
    # 从当前文件夹下的main文件夹(from .main)引入main包(import main)作为main蓝本(as main_blueprint)
    from .main import main as main_blueprint
    # 通过Flask程序实例app 提供的 register_blueprint() 方法注册蓝本，参数为 蓝本名_blueprint
    app.register_blueprint(main_blueprint)

    # 注册后台蓝本
    # 从当前文件夹下的admin文件夹(from .admin)引入admin包(import admin)作为admin蓝本(as admin_blueprint)
    from .admin import admin as admin_blueprint
    # 通过Flask程序实例app 提供的 register_blueprint() 方法注册蓝本，参数为 蓝本名_blueprint，同时增加蓝本前缀 /admin
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # 最后，返回Flask程序实例app 
    return app