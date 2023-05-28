from dao.Database import db


# 表示 GitHub issue 的标签
class Label(db.Model):
    def __init__(self, init_dict):
        self.id = init_dict['id']
        self.node_id = init_dict['node_id']
        self.url = init_dict['url']
        self.name = init_dict['name']
        self.color = init_dict['color']
        self.default = init_dict['default']
        self.description = init_dict['description']

    __tablename__ = "label"
    id = db.Column(db.BigInteger, primary_key=True)
    node_id = db.Column(db.String(255), nullable=False)
    url = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(64), nullable=False)
    default = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text, nullable=True)
    # category 新增一个属性。便于聚集各个子标签，初始化时不填，通过解析description得到
