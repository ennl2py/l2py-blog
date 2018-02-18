import os

# 定义项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))

# 定义Config类，包含各编程环境通用配置条件
class Config:
    # SECRET_KEY 的作用主要是提供一个值做各种 HASH（主要的作用应该是加密过程中作为算法的一个参数）
    # 这个值的复杂度也就影响到了数据传输和存储时的复杂度
    # 考虑到安全性, 这个密钥是不建议明文存储在程序中的. 最好的方法是存储在系统环境变量中
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this my blog app golb ym siht'

    # SQLALCHEMY_COMMIT_ON_TEARDOWN 设置为 True 可以在数据库请求执行完逻辑之后自动commit
    # SQLALCHEMY_COMMIT_ON_TEARDOWN 设置为 Flase 需要通过手动执行 db.session.commit() 进行数据库操作提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # SQLALCHEMY_TRACK_MODIFICATIONS 默认设置为True，将会追踪对象的修改并且发送信号，这需要额外的内存，如果不必要的可以禁用它
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

# 开发环境配置项
class DevelopmentConfig(Config):
    DEBUG = True # DEBUG 追踪网站信息，建议在开发环境开启

    # SQLAlchemy连接数据库的一般格式为database_type + driver: // user: password @ sql_server_ip:port / database_name
    # SQLALCHEMY连接mysql数据库
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:8114193@localhost/l2py_db'

    # SQLALCHEMY连接sqlite数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-database.sqlite')

# 生产环境配置项
class ProductionConfig(Config):
    pass

# config字典注册不同配置环境，默认为开发环境DevelopmentConfig
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
