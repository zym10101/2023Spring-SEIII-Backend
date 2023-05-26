from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

db = SQLAlchemy()


def save(issues):
    for issue in issues:
        self.c.save(db.session, issue)
    db.session.commit()
