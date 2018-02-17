from . import admin
# 引入db数据库实例和各数据模型
from .. import db
from ..models import Admin, Article, Category, User, Comment, Reply
from flask import render_template, redirect, request, url_for, flash
from ..some_func import ch_content

# 后台登录页
@admin.route('/login')
def login():
    return render_template('admin/login.html')

# 后台首页
@admin.route('/')
def index():
    # 文章总数
    articles = len(Article.query.all())
    # 评论总数（一级回复总数+二级回复总数）
    comments = len(Comment.query.all()) + len(Reply.query.all())
    # 用户总数
    users = len(User.query.all())
    return render_template('admin/index.html', articles=articles, comments=comments, users=users)

# 文章页面
@admin.route('/article')
def article():
    # 将数据库中的所有文章按创建时间倒序排列
    articles = Article.query.order_by(Article.created_time.desc()).all()
    return render_template('admin/article.html', articles=articles)

# 文章添加页面
@admin.route('/add/article', methods=['GET', 'POST'])
def add_article():
    # 添加文章或者修改文章时，需要使用到文章分类选择
    categorys = Category.query.all()
    # 如果提交的文章标题或者文章内容为空，则返回原页面，否则将数据写入数据库
    if request.method == "POST" and request.form['title'] and request.form['content'] != '':
        new_article = Article(title=request.form['title'], content=request.form['content'], abstract=ch_content(request.form['content'])[:137]+'...',
                              category_id=request.form['category'])
        db.session.add(new_article)
        return redirect(url_for('admin.article'))
    return render_template('admin/addarticle.html', categorys=categorys)

# 文章编辑页面
@admin.route('/edit/article/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    categorys = Category.query.all()
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.content = request.form['content']
        article.abstract = ch_content(request.form['content'])[:137]+'...'
        article.category_id = request.form['category']
        db.session.add(article)
        return redirect(url_for('admin.article'))
    return render_template('admin/editearticle.html', categorys=categorys, article=article)

# 文章删除
@admin.route('/delete/article/<int:id>')
def del_article(id):
    # 删除文章时，删除相关联的一级回复和二级回复
    article = Article.query.get_or_404(id)
    article_comments = Comment.query.filter_by(article_id=id).all()
    for each_comment in article_comments:
        comment_replys = Reply.query.filter_by(comment_id=each_comment.id).all()
        for each_reply in comment_replys:
            db.session.delete(each_reply)
        db.session.delete(each_comment)
    db.session.delete(article)
    return redirect(url_for('admin.article'))

# 文章分类页面
@admin.route('/category', methods=['GET', 'POST'])
def category():
    # 如果提交表单且分类名不为空
    if request.method == 'POST' and request.form['category']:
        new_category = Category(name=request.form['category'])
        db.session.add(new_category)
        return redirect(url_for('admin.category'))
    categorys = Category.query.order_by(Category.id).all()
    return render_template('admin/category.html', categorys=categorys)

# 文章分类删除
@admin.route('/delete/category/<int:id>')
def del_category(id):
    category = Category.query.get_or_404(id)
    # 如果该分类下没有文章，则删除分类
    if len(category.articles) == 0:
        db.session.delete(category)
        return redirect(url_for('admin.category'))

# 用户页面
@admin.route('/user')
def user():
    users = User.query.all()
    return render_template('admin/user.html', users=users)

# 文章评论页面
@admin.route('/article/<int:id>/comments')
def article_comments(id):
    title = Article.query.get_or_404(id).title
    comments = Comment.query.filter_by(article_id=id).all()
    return render_template('admin/comment.html', comments=comments, title=title, id=id)

# 一级回复屏蔽
@admin.route('/shield/comment/<int:id>')
def shield_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.status = False
    db.session.add(comment)
    article = Article.query.filter_by(id=comment.article_id).first()
    title = article.title
    id = article.id
    comments = Comment.query.filter_by(article_id=comment.article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=id))

# 一级回复取消屏蔽
@admin.route('/unshield/comment/<int:id>')
def unshield_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.status = True
    db.session.add(comment)
    article = Article.query.filter_by(id=comment.article_id).first()
    title = article.title
    id = article.id
    comments = Comment.query.filter_by(article_id=comment.article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=id))

# 二级回复屏蔽
@admin.route('/shield/reply/<int:id>')
def shield_reply(id):
    reply = Reply.query.get_or_404(id)
    reply.status = False
    db.session.add(reply)
    article_id = Comment.query.filter_by(id=reply.comment_id).first().article_id
    title = Article.query.filter_by(id=article_id).first().title
    comments = Comment.query.filter_by(article_id=article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=article_id))

# 二级回复取消屏蔽
@admin.route('/unshield/reply/<int:id>')
def unshield_reply(id):
    reply = Reply.query.get_or_404(id)
    reply.status = True
    db.session.add(reply)
    article_id = Comment.query.filter_by(id=reply.comment_id).first().article_id
    title = Article.query.filter_by(id=article_id).first().title
    comments = Comment.query.filter_by(article_id=article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=article_id))

