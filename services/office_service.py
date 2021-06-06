import json
import os
from services.expand_service import ExpandService


PATH = '/home/woowup/Escritorio/glideapp/offices.json'


class OfficeService(ExpandService):
    def __init__(self):
        super(OfficeService, self).__init__()
        self.path = os.getenv('OFFICES_FILE')


    def fetch(self, url=None, params=None):
        with open(self.path, 'r') as f:
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
