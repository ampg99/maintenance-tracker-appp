from ..model.user import UserStore, Requests, AdminFeedback
from ..model.models import SuperUser


class MainDB:
    """The main db class"""
    def __init__(self):
        
        self.users = UserStore()
        self.requests = Requests()
        self.feedback = AdminFeedback()
        self.users.insert(SuperUser.admin_details())

    def clear(self):
        self.users.clear()
        self.requests.clear()
        self.feedback.clear()