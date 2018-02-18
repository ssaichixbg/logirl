import inspect
# decorator
def GET(func):
    def wrapper(self):
        keys = [k for k in inspect.getargspec(func).args if not k == 'self']
        GETs = self.request.GET
        params = {k: GETs.getlist(k) if len(GETs.getlist(k)) > 1 else GETs.get(k)
                  for k in set(keys).intersection(GETs.keys())}

        if not keys:
            params = {k: GETs.getlist(k) if len(GETs.getlist(k)) > 1 else GETs.get(k)
                  for k in GETs.keys()}

        return func(self, **params)

    return wrapper