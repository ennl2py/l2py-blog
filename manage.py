from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
# 如果你想要在shell里操作相应的数据模型，需要提前引入
from app.models import Admin, User, Category, Article, Comment, Reply

# 拿到app实例
app = create_app('default')
# 把Flask程序实例app作为参数传递给 flask_script 提供的 Manager类，初始化Manager实例 manager
# 之后通过manager来进行app实例操作，如服务启动、端口重置等
manager = Manager(app)
# 把Flask程序实例app和SQLAlchemy实例db作为参数传递给 flask_migrate 提供的 Migrate类，初始化Migrate实例 migrate
migrate = Migrate(app, db)

# 定义Python Shell的上下文，将引入的数据模型添加到app和db之后
def make_shell_context():
    return dict(app=app, db=db, Admin=Admin, User=User, Category=Category, Article=Article, Comment=Comment, Reply=Reply)
# 增加 manage.py 的 shell 命令，内容为上述定义的上下文
manager.add_command("shell", Shell(make_context=make_shell_context))
# 增加 manage.py 的 db 命令，内容为 flask_migrate 提供的 MigrateCommand类
manager.add_command('db', MigrateCommand)

# 启动程序
if __name__ == '__main__':
    manager.run()