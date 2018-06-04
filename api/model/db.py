from ..model.user import UserStore, Requests
from ..model.models import SuperUser


class MainDB:
    def __init__(self):
        self.users = UserStore()
        self.requests = Requests
        self.users.insert(SuperUser.admin_details())

    def clear(self):
        self.users.clear()
        self.users.insert(SuperUser.admin_details())