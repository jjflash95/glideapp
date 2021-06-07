import json
from services.expand_service import ExpandService


class OfficeService(ExpandService):
    def __init__(self, url):
        super(OfficeService, self).__init__()
        self.url = url

    def fetch(self, url=None, params=None):
        with open(self.url, 'r') as f:
            data = json.loads(f.read())
            offices = {office.get('id'): office for office in data}
        return offices

    def all(self, limit=100, offset=0):
        return self.fetch().values()[offset:offset + limit]

    def get(self, office_id):
        if not type(office_id) == set:
            office_id = set(office_id)

        offices = self.fetch()
        return [offices.get(offid) for offid in office_id]
