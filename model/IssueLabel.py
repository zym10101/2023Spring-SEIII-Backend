from dao.Database import db

# 解决 issue 与 label 的多对多关系
IssueLabel = db.Table('issue_label',
                      db.Column('issue_id', db.BigInteger, db.ForeignKey('issue.id'), primary_key=True),
                      db.Column('label_id', db.BigInteger, db.ForeignKey('label.id'), primary_key=True)
                      )
