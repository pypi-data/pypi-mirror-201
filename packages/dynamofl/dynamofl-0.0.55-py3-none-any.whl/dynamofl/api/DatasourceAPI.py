class DatasourceAPI:
    def __init__(self, request):
        self.request = request

    def get_datasources(self):
        j = self.request._make_request('GET', '/datasources')
        return j['data']

    def get_datasource(self, key):
        return self.request._make_request(
            'GET', '/datasources', params={'key': key}, list=True)

    def create_datasource(self, params):
        return self.request._make_request('POST', '/datasources', params=params)

    def connect_datasource(self, key, params):
        return self.request._make_request('POST', f'/datasources/{key}', params=params)

    def delete_datasource(self, key):
        return self.request._make_request('DELETE', f'/datasources/{key}')

    def create_trainers(self, key, params):
        return self.request._make_request('POST', f'/datasources/{key}/trainers', params=params)
