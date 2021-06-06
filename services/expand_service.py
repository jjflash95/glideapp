

class ExpandService:
    def __init__(self):
        self.hooks = {}

    def registerhook(self, key, hook):
        self.hooks[key] = hook

    def gethook(self, key):
        return self.hooks[key]

    def getcurrent(self, expand):
        if type(expand) == str:
            expand = expand.split('.')

        return expand[0], expand[1:]

    def tohashtable(self, data):
        return {d.get('id'): d for d in data if d.get('id')}

    def getids(self, key, data):
        print(key, data)
        return {d.get(key) for d in data if d.get(key)}

    def _expand(self, data, expand=None):
        if not expand:
            return data

        key, expand = self.getcurrent(expand)
        fetchkeys = self.getids(key, data)

        if not fetchkeys:
            return data

        hook = self.gethook(key)
        newdata = hook(fetchkeys)
        result = self._expand(newdata, expand)

        if not result:
            return data

        result = self.tohashtable(result)
        for d in data:
            d[key] = result.get(d[key])

        return data

    def expand(self, data, expansions=None):
        if not data:
            return data
        if not expansions:
            return data

        for expand in expansions:
            data = self._expand(data, expand)

        return data
