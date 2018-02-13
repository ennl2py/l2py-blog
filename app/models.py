from . import db
from datetime import datetime


# 定义管理员类，将在连接的数据库中创建管理员数据表
class Admin(db.Model):
    # __tablename__ 定义在数据表的表名
    __tablename__ = 'admins'
    # 管理员id，这一行需要默认定义primary_key属性为True，表示id为主键
    id = db.Column(db.Integer, primary_key=True)
    # 管理员用户名，定义unique属性为True，表示用户名不能重复
    a_name = db.Column(db.String(64), unique=True)
    # 管理员密码
    a_password = db.Column(db.String(18))


# 定义用户类，将在连接的数据库中创建用户数据表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    u_name = db.Column(db.String(64))
    # 用户头像地址
    avatar_url = db.Column(db.String(128))
    # 用户注册的第三方渠道，例如是来自github还是weibo
    social_type = db.Column(db.String(30))


# 定义文章类别类，将在连接的数据库中创建文章分类表
class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    # 分类名，定义unique属性为True，表示分类名不能重复
    name = db.Column(db.String(64), unique=True)
    # 一个文章分类下可以有多篇文章，所以这是一个 一对多 的关系
    # 添加到Category模型中的articles属性代表这个关系的面向对象视角
    # 对于一个Category类的实例，其articles属性将返回与文章类中与文章分类想关联的所有文章组成的列表
    # db.relationship()的第一个参数表明这个关系的另一端是哪个模型
    # backref 参数则向 Article 模型添加一个 category 属性，从而定义反向关系
    articles = db.relationship('Article', backref='category')


# 定义文章类，将在数据库中创建文章数据表
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    # 标题，定义unique属性为True，表示标题不允许出现重复值
    title = db.Column(db.String(80), unique=True)
    # 发布时间，定义default属性为datetime.now，设置默认值为创建时间
    created_time = db.Column(db.DateTime, default=datetime.now)
    # 文章内容，定义nullable属性为Flase，表示不允许出现空内容
    content = db.Column(db.Text, nullable=False)
    # 文章摘要
    abstract = db.Column(db.String(140), nullable=False)
    # 阅读量
    reading_time = db.Column(db.Integer, default=0)
    # 文章分类id，一个分类对应多个文章
    # category_id 列被定义为外键，这个外键连接了categorys表中的id列和users表中的category_id列
    # 传给db.ForeignKey()的参数'category_id'表示这列的值是categorys表中id列的值
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    # 文章所对应的一级回复关系定义，一篇文章对应多个一级回复
    comments = db.relationship('Comment', backref='article')


# 定义一级回复类，将在数据库中创建一级回复数据表
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    # 一级回复用户的用户名
    author = db.Column(db.String(64))
    # 一级回复用户的id
    author_id = db.Column(db.Integer)
    # 一级回复用户的头像地址
    avatar_url = db.Column(db.String(128))
    # 一级回复的创建时间
    created_time = db.Column(db.DateTime, default=datetime.now)
    # 一级回复内容
    content = db.Column(db.Text, nullable=False)
    # 一级回复的状态，是否允许被显示，默认定义值为True，表示可以正常显示
    status = db.Column(db.Boolean, default=True)
    # 一级回复所对应的文章id，一篇文章对应多个一级回复
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    # 一级回复下的二级回复关系定义，一个一级回复对应多个二级回复
    replys = db.relationship('Reply', backref='comment')


# 定义二级回复类，将在数据库中创建二级回复数据表
class Reply(db.Model):
    __tablename__ = 'replys'
    id = db.Column(db.Integer, primary_key=True)
    # 二级回复用户的用户名
    author = db.Column(db.String(64))
    # 二级回复用户的id
    author_id = db.Column(db.Integer)
    # 二级回复被回复用户的用户名
    to_author = db.Column(db.String(64))
    # 二级回复被回复用户的id
    to_author_id = db.Column(db.Integer)
    # 二级回复用户的头像地址
    avatar_url = db.Column(db.String(128))
    # 二级回复的创建时间
    created_time = db.Column(db.DateTime, default=datetime.now)
    # 二级回复内容
    content = db.Column(db.Text, nullable=False)
    # 二级回复的状态，是否允许被显示，默认定义值为True，表示可以正常显示
    status = db.Column(db.Boolean, default=True)
    # 二级回复所对应的一级回复id，一个一级回复对应多个二级回复
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))