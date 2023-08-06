import json

import requests

API_VERSION = 'v1'

def _check_for_error(r):
    if not r.ok:
        print(json.dumps(json.loads(r.text), indent=4))
    r.raise_for_status()

class _Request:
    def __init__(self, token, host):
        self.token = token
        self.host = host

    def _get_route(self):
        return f'{self.host}/{API_VERSION}'

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.token}'}

    def _make_request(self, method, url, params=None, files=None, list=False, print_error=True):
        if method == 'POST':
            r = requests.post(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                json=params,
                files=files
            )
        elif method == 'GET':
            r = requests.get(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                params=params
            )
        elif method == 'DELETE':
            r = requests.delete(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                json=params
            )

        if print_error:
            _check_for_error(r)

        if r.content:
            if list:
                return r.json()['data']
            else:
                return r.json()