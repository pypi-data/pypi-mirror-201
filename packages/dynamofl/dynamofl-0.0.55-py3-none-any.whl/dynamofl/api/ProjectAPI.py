import os
import pathlib
import requests


class ProjectAPI:
    def __init__(self, request):
        self.request = request

    def create_project(self, params=None):
        return self.request._make_request('POST', '/projects', params=params)

    def get_info(self, key):
        return self.request._make_request('GET', f'/projects/{key}')

    def get_projects(self):
        return self.request._make_request('GET', '/projects', list=True)

    def update_rounds(self, key, rounds):
        return self.request._make_request('POST', f'/projects/{key}', params={'rounds': rounds})

    def update_schedule(self, key, schedule):
        return self.request._make_request('POST', f'/projects/{key}', params={'schedule': schedule})

    def update_paused(self, key, paused):
        return self.request._make_request('POST', f'/projects/{key}', params={'paused': paused})

    def update_auto_increment(self, key, auto_increment):
        return self.request._make_request('POST', f'/projects/{key}', params={'autoIncrement': auto_increment})

    def update_optimizer_params(self, key, optimizer_params):
        return self.request._make_request('POST', f'/projects/{key}', params={'optimizerParams': optimizer_params})

    def update_contributor(self, key, email, role):
        return self.request._make_request('POST', f'/projects/{key}/contributors/{email}', params={'role': role})

    def delete_project(self, key):
        return self.request._make_request('DELETE', f'/projects/{key}')

    def add_contributor(self, key, email, role='member'):
        return self.request._make_request('POST', f'/projects/{key}/contributors', params={'email': email, 'role': role})

    def delete_contributor(self, key, email):
        return self.request._make_request('DELETE', f'/projects/{key}/contributors', params={'email': email})

    def get_next_schedule(self, key):
        return self.request._make_request('GET', f'/projects/{key}/schedule')

    def increment_round(self, key):
        return self.request._make_request('POST', f'/projects/{key}/increment')

    def get_rounds(self, key):
        return self.request._make_request('GET', f'/projects/{key}/rounds', list=True)

    def get_round(self, key, round):
        return self.request._make_request('GET', f'/projects/{key}/rounds/{round}')

    def get_stats(self, key, params={}):
        return self.request._make_request('GET', f'/projects/{key}/stats', params, list=True)

    def get_stats_avg(self, key):
        return self.request._make_request('GET', f'/projects/{key}/stats/avg')

    def get_submissions(self, key, params={}):
        return self.request._make_request('GET', f'/projects/{key}/submissions', params, list=True)

    def upload_optimizer(self, key, path):
        with open(path, 'rb') as f:
            self.request._make_request(
                'POST', f'/projects/{key}/optimizers', files={'optimizer': f})

    def upload_file(self, key, path):
        with open(path, 'rb') as f:
            self.request._make_request(
                'POST', f'/projects/{key}/files', files={'file': f})

    def report_stats(self, key, stats):
        return self.request._make_request('POST', f'/projects/{key}/stats', params=stats)

    def get_presigned_upload_url_vertical(self, key, datasource_key, round, mode):
        return self.request._make_request('POST', f'/projects/{key}/vertical/upload', {
            'round': round,
            'datasourceKey': datasource_key,
            'mode': mode,
        })['url']

    def verify_upload_vertical(self, key, datasource_key, round, mode):
        return self.request._make_request('POST', f'/projects/{key}/vertical/verify', {
            'round': round,
            'datasourceKey': datasource_key,
            'mode': mode,
        })

    def get_presigned_download_url_vertical(self, key, datasource_key, round, mode):
        return self.request._make_request('POST', f'/projects/{key}/vertical/download', {
            'round': round,
            'datasourceKey': datasource_key,
            'mode': mode,
        })['url']

    """
    Bridge APIs
    """

    def create_bridge(self, params):
        return self.request._make_request('POST', '/bridges', params=params)

    def get_bridges_for_datasource(self, datasource_key):
        return self.request._make_request(
            'GET', '/bridges', params={'datasourceKey': datasource_key})

    def get_bridges_for_project(self, project_key):
        return self.request._make_request(
            'GET', '/bridges', {'projectKey': project_key}, list=True)

    def get_bridge_of_project_and_datasource(self, project_key, datasource_key):
        return self.request._make_request('GET', '/bridges', params={
            'projectKey': project_key,
            'datasourceKey': datasource_key
        })

    """
    Moved from Projects
    """

    def pull_model(self, project_key, filepath, datasource_key=None, round=None, federated_model=None):
        params = {
            'usePresignedUrl': True
        }
        if round is not None:
            params['round'] = round
        if federated_model is not None:
            params['federatedModel'] = federated_model

        if datasource_key is None:
            url = f'/projects/{project_key}/models'
        else:
            url = f'/projects/{project_key}/models/{datasource_key}'
        download_url = self.request._make_request(
            'GET', url, params=params)['url']
        directory = os.path.dirname(filepath)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        r = requests.get(download_url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=None):
                f.write(chunk)

    def push_model(self, project_key, path, datasource_key, params=None):
        if params is not None:
            self.request._make_request(
                'POST', f'/projects/{project_key}/models/{datasource_key}/params', params={'params': params})

        if datasource_key is None:
            url = f'/projects/{project_key}/models'
        else:
            url = f'/projects/{project_key}/models/{datasource_key}'
        with open(path, 'rb') as f:
            file_name = os.path.basename(path)
            params = {
                'filename':  file_name,
                'datasourceKey': datasource_key
            }
            upload_url = self.request._make_request(
                'GET', f'/projects/{project_key}/models/presigned-url', params=params)['url']
            r = requests.put(upload_url, data=f.read())
            if not r.ok:
                print(r.text)
            r.raise_for_status()

            try:
                self.request._make_request('POST', url, print_error=False)
            except Exception as e:
                if str(e).find('Model will not be uploaded.'):
                    print('Model not sampled.')
                else:
                    raise e

    def push_ids(self, project_key, base_file):
        with open(base_file, 'rb') as f:
            try:
                self.request._make_request(
                    'POST', f'/projects/{project_key}/ids', files={'ids': f})
            except Exception as e:
                print('Something went wrong')
