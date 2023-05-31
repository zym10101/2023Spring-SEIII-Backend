from dao.Database import db


# 表示该 GitHub issue 的作者的相关信息
class User(db.Model):
    def __init__(self, init_dict):
        self.login = init_dict['login']
        self.id = init_dict['id']
        self.node_id = init_dict['node_id']
        self.avatar_url = init_dict['avatar_url']
        self.gravatar_id = init_dict['gravatar_id']
        self.url = init_dict['url']
        self.html_url = init_dict['html_url']
        self.followers_url = init_dict['followers_url']
        self.following_url = init_dict['following_url']
        self.gists_url = init_dict['gists_url']
        self.starred_url = init_dict['starred_url']
        self.subscriptions_url = init_dict['subscriptions_url']
        self.organizations_url = init_dict['organizations_url']
        self.repos_url = init_dict['repos_url']
        self.events_url = init_dict['events_url']
        self.received_events_url = init_dict['received_events_url']
        self.type = init_dict['type']
        self.site_admin = init_dict['site_admin']

    __tablename__ = "user"
    # GitHub用户名
    login = db.Column(db.Text, nullable=False)
    # 用户ID
    id = db.Column(db.Integer, primary_key=True)
    # 用户节点ID
    node_id = db.Column(db.Text, nullable=False)
    # 头像链接
    avatar_url = db.Column(db.Text, nullable=False)
    # Gravatar ID
    gravatar_id = db.Column(db.Text, nullable=True)
    # 用户 GitHub API 链接
    url = db.Column(db.Text, nullable=False)
    # 用户 GitHub 主页链接
    html_url = db.Column(db.Text, nullable=False)
    # 用户关注者的 GitHub API 链接
    followers_url = db.Column(db.Text, nullable=False)
    # 用户正在关注的人的 GitHub API 链接
    following_url = db.Column(db.Text, nullable=False)
    # 用户 Gists 的 GitHub API 链接
    gists_url = db.Column(db.Text, nullable=False)
    # 用户收藏的项目的 GitHub API 链接
    starred_url = db.Column(db.Text, nullable=False)
    # 用户订阅的仓库的 GitHub API 链接
    subscriptions_url = db.Column(db.Text, nullable=False)
    # 用户所在的组织的 GitHub API 链接
    organizations_url = db.Column(db.Text, nullable=False)
    # 用户仓库的 GitHub API 链接
    repos_url = db.Column(db.Text, nullable=False)
    # 用户 GitHub 活动的 GitHub API 链接
    events_url = db.Column(db.Text, nullable=False)
    # 用户收到的 GitHub 活动的 GitHub API 链接
    received_events_url = db.Column(db.Text, nullable=False)
    # 用户类型（"User" 或 "Organization"）
    type = db.Column(db.Text, nullable=False)
    # 用户是否为 GitHub 网站管理员
    site_admin = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'login': self.login,
            'id': self.id,
            'node_id': self.node_id,
            'avatar_url': self.avatar_url,
            'gravatar_id': self.gravatar_id,
            'url': self.url,
            'html_url': self.html_url,
            'followers_url': self.followers_url,
            'following_url': self.following_url,
            'gists_url': self.gists_url,
            'starred_url': self.starred_url,
            'subscriptions_url': self.subscriptions_url,
            'organizations_url': self.organizations_url,
            'repos_url': self.repos_url,
            'events_url': self.events_url,
            'received_events_url': self.received_events_url,
            'type': self.type,
            'site_admin': self.site_admin
        }
