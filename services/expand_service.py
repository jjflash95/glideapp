
class MissingHookException(Exception):
    pass


class ExpandService:
    def __init__(self):
        self._hooks = {}

    def registerhook(self, key, hook):
        self._hooks[key] = hook

    def gethook(self, key):
        if not key in self._hooks:
            raise MissingHookException(key)

        return self._hooks[key]

    def nextexpansion(self, expand):
        if type(expand) == str:
            expand = expand.split('.')

        return expand[0], expand[1:]

    def indexbyid(self, data):
        return {d.get('id'): d for d in data if d.get('id')}

    def getkeys(self, key, data):
        return {d.get(key) for d in data if d.get(key)}

    def _expand(self, data, expand=None):
        if not expand:
            return data

        key, expand = self.nextexpansion(expand)
        fetchkeys = self.getkeys(key, data)

        if not fetchkeys:
            return data

        newdata = self.gethook(key)(fetchkeys)
        result = self._expand(newdata, expand)

        if not result:
            return data

        result = self.indexbyid(result)
        
        for d in data:
            d[key] = result.get(d[key])

        return data

    def expand(self, data, expansions=None):
        if not data or not expansions:
            return data

        for expand in expansions:
            data = self._expand(data, expand)

        return data
