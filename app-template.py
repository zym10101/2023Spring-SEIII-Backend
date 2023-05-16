from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# 使用Flask类创建一个app对象
# __name__：代表当前app.py这个模块
# 1. 以后出现bug可以帮助快速定位
# 2. 对于寻找模板文件有一个相对路径
app = Flask(__name__)

load_dotenv()
DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
DB_PORT = os.environ.get('DB_PORT')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] \
    = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}?charset=utf8"

# 在app.config中设置好连接数据库的信息,
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中连接数据库的信息
db = SQLAlchemy(app)


# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute("select * from tmp")
#         print(rs.fetchone())


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


user = User(username="wangwu", password="123456")
with app.app_context():
    db.create_all()
    # with db.engine.connect() as conn:
    #     rs = conn.execute("select * from tmp")
    #     print(rs.fetchone())


@app.route("/user/add")
def user_add():
    # 1.创建ORM对象
    user_ = User(username="zhangsan", password="123456")
    # 2.将ORM对象添加到db.session中
    db.session.add(user_)
    # 3.commit操作
    db.session.commit()
    return "用户创建成功!"


@app.route("/user/query")
def user_query():
    # 1.get查找：根据主键查找
    # user_ = User.query.get(1)
    # print(f"{user_.id}, {user_.username}, {user_.password}")
    # 2.filter_by查找：返回flask_sqlalchemy.query.Query类数组
    users = User.query.filter_by(username="zhangsan")
    for u in users:
        print(f"{u.id}, {u.username}, {u.password}")
    return "数据查找成功!"


@app.route("/user/update")
def user_update():
    user_ = User.query.filter_by(username="zhangsan").first()
    user_.password = "222222"
    db.session.commit()
    return "数据修改成功!"


@app.route("/user/delete")
def user_delete():
    user_ = User.query.filter_by(username="zhangsan").first()
    db.session.delete(user_)
    db.session.commit()
    return "数据删除成功!"


# 创建路由和视图函数的映射
@app.route("/")
def root():
    # jinja2
    return render_template('Index.html')


@app.route("/profile")
def blog_list():
    return "我是博客列表！"


@app.route("/blog/<int:blog_id>")
def blog_detail():
    return f"您访问的博客是：{blog_id}"


@app.route("/book/list")
def book_list():
    # request.args：类字典类型
    page = request.args.get("page", default=1, type=int)
    return f"您获取的是第{page}页图书列表"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
