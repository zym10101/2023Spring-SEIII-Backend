from dao.Database import db


# 本系统的账号信息
class Account(db.Model):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
