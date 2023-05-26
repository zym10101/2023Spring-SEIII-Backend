from dao.saveStrategy.AbstractSaveStrategy import AbstractSaveStrategy


class MysqlSaveStrategy(IssueSaveStrategy):
    def __init__(self, database, c):
        self.db = database
        # 待存储的类，该类需要实现save方法
        self.c = c

    def save(self, issues):
        for issue in issues:
            self.c.save(self.db.session, issue)
        self.db.session.commit()
