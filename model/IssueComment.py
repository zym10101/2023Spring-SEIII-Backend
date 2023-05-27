from dao.Database import db

# 解决 issue 与 comment 的多对多关系
IssueComment = db.Table('issue_comment',
                        db.Column('issue_id', db.BigInteger, db.ForeignKey('issue.id'), primary_key=True),
                        db.Column('comment_id', db.BigInteger, db.ForeignKey('comment.id'), primary_key=True)
                        )
