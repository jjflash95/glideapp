import json
from services.expand_service import ExpandService


class DepartmentService(ExpandService):
    def __init__(self, url):
        super(DepartmentService, self).__init__()
        self.url = url

    def fetch(self, url=None, params=None):
        with open(self.url, 'r') as f:
            data = json.loads(f.read())
            departments = {dept.get('id'): dept for dept in data}
        return departments

    def all(self, limit=100, offset=0):
        return self.fetch().values()[offset:offset + limit]

    def get(self, dept_id):
        if not type(dept_id) == set:
            dept_id = set(dept_id)

        departments = self.fetch()
        return [departments.get(dept) for dept in dept_id]
