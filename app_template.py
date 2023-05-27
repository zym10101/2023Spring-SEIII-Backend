from flask import Flask, render_template, request, jsonify
from dao.Database import db
from utils.Env import DB_HOSTNAME, DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_PORT, ACCESS_TOKEN

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] \
    = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"
db.init_app(app)
