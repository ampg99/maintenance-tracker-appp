from ..model.user import UserStore
from ..model.models import SuperUser


class MainDB:
    def __init__(self):
        self.users = UserStore()
        #self.requests = Requests()
        self.blacklist = set()

    def clear(self):
        self.users.clear()
