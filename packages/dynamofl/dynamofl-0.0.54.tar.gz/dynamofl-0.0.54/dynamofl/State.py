import os
from time import sleep
from importlib import import_module

from dynamofl.api.DatasourceAPI import DatasourceAPI
from dynamofl.Request import _Request

from .api.ProjectAPI import ProjectAPI
from .Project import _Project
from .Datasource import _Datasource


class _State:
    def __init__(self, token, host='https://api.dynamofl.com', metadata=None):

        self.token = token
        self.host = host

        # Vertical
        self.label_participants = []
        self.feature_participants = []

        self.datasources = {}
        self.instance_id = None
        self.metadata = metadata

        self.request = _Request(host=host, token=token)

        self.project_api = ProjectAPI(self.request)
        self.datasource_api = DatasourceAPI(self.request)

    def _get_last_fed_model_round(self, current_round, is_complete):
        if is_complete:
            return current_round
        else:
            return current_round - 1

    def _check_if_model_downloaded(self, federated_model_path):
        return os.path.exists(federated_model_path)
    
    def test_callback(self, j, _):
        '''
        Condition: yes_stats <- False
        '''
        test_samples = list(j['data']['testSamples'].keys()) if 'testSamples' in j['data'] else []
        
        for datasource_key in test_samples:
            project_info = j['data']['project']
            trainer_key = j['data']['testSamples'][datasource_key]['trainerKey']

            project_key = project_info['key']
            project = _Project(key=project_key, api=self.project_api)

            # on some project round completed
            # get appropriate train, test methods

            if trainer_key not in self.datasources[datasource_key].trainers and not project_info['hasDynamicTrainer']:
                return

            if project_info['hasDynamicTrainer']:
                mod = import_module(f'dynamic_trainers.{project_key}.train')
                test = getattr(mod, 'test')
            else:    
                test = self.datasources[datasource_key].trainers[trainer_key]['test']
            model_path = 'models'
            if 'model_path' in self.datasources[datasource_key].trainers.get(trainer_key, {}):
                model_path = self.datasources[datasource_key].trainers[trainer_key]['model_path']

            model_extension = project_info['modelType']
            current_round = project_info['currentRound']
            prev_round = self._get_last_fed_model_round(current_round, project_info['isComplete'])
            federated_model_path = get_federated_path(project_key, model_path, model_extension, datasource_key, prev_round)

            if not self._check_if_model_downloaded(federated_model_path):
                # Pull
                print(f'>>> ({project_key}-{datasource_key}) Waiting to download round ({prev_round}) federated model...')
                project.pull_model(federated_model_path, round=prev_round, datasource_key=datasource_key, federated_model=True)

            # Test
            print(f'>>> ({project_key}-{datasource_key}) Running validation on round ({prev_round}) federated model...')
            test_res = test(datasource_key, federated_model_path, project_info)
            if test_res is not None:
                scores, num_samples = test_res
                print(scores)
                print(f'>>> ({project_key}-{datasource_key}) Uploading scores...')
                project.report_stats(scores, num_samples, prev_round, datasource_key)
                print('Done.')
            print()


    def train_callback(self, j, _):
        '''
        Conditions: yes_submission <- False
        '''
        train_samples = list(j['data']['trainSamples'].keys()) if 'trainSamples' in j['data'] else []
        
        for datasource_key in train_samples:
            project_info = j['data']['project']
            trainer_key = j['data']['trainSamples'][datasource_key]['trainerKey']
            hyper_param_values = j['data']['trainSamples'][datasource_key]['hyperParamValues']

            project_key = project_info['key']
            project = _Project(key=project_key, api=self.project_api)

            # on some project round completed
            # get appropriate train, test methods

            if trainer_key not in self.datasources[datasource_key].trainers and not project_info['hasDynamicTrainer']:
                return
            if project_info['hasDynamicTrainer']:
                mod = import_module(f'dynamic_trainers.{project_key}.train')
                train = getattr(mod, 'train')
            else:    
                train = self.datasources[datasource_key].trainers[trainer_key]['train']
            model_path = 'models'
            if 'model_path' in self.datasources[datasource_key].trainers.get(trainer_key, {}):
                model_path = self.datasources[datasource_key].trainers[trainer_key]['model_path']

            model_extension = project_info['modelType']
            current_round = project_info['currentRound']
            prev_round = self._get_last_fed_model_round(current_round, project_info['isComplete'])
            federated_model_path = get_federated_path(project_key, model_path, model_extension, datasource_key, prev_round)

            if not self._check_if_model_downloaded(federated_model_path):
                # Pull
                print(f'>>> ({project_key}-{datasource_key}) Waiting to download round ({prev_round}) federated model...')
                project.pull_model(federated_model_path, round=prev_round, datasource_key=datasource_key, federated_model=True)

            # Train and push
            new_model_path = get_trained_path(project_key, model_path, model_extension, datasource_key, current_round)

            print(f'>>> ({project_key}-{datasource_key}) Training weights on local model...')
            train_res = train(datasource_key, federated_model_path, new_model_path, project_info, hyper_param_values)

            print(f'>>> ({project_key}-{datasource_key}) Uploading round ({current_round}) trained model...')
            if train_res:
                project.push_model(new_model_path, datasource_key, params=train_res)
            else:
                project.push_model(new_model_path, datasource_key)
            print('Done.')
            print()


    # creates a new datasource in the api
    def attach_datasource(self, key, name=None, metadata=None, type=None):

        while not self.instance_id:
            sleep(0.1)

        params = {'key': key, 'instanceId': self.instance_id}
        if name is not None:
            params['name'] = name
        if self.metadata is not None:
            params['metadata'] = self.metadata
        if metadata is not None:
            params['metadata'] = metadata
        if type is not None and type != 'horizontal':
            # Valid types are 'label' and 'feature'
            params['type'] = type

        try:
            # Datasource exists so update it
            self.datasource_api.connect_datasource(key, params)
            print(f'>>> Updated datasource "{key}"')
        except:
            # Datasource doesn't exist so create it
            self.datasource_api.create_datasource(params=params)
            print(f'>>> Created datasource "{key}"')

        ds = _Datasource(key, type, api=self.datasource_api)
        self.datasources[key] = ds

        return ds

    def delete_datasource(self, key):
        return self.datasource_api.delete_datasource(key)

    def delete_project(self, key):
        return _Project(key, api=self.project_api).delete_project()

    def get_user(self):
        return self.request._make_request('GET', '/user')

    def create_project(self, base_file, params, dynamic_trainer_path=None, type=None):
        project = _Project(params=params, api=self.project_api)
        if type == 'horizontal':
            project.push_model(base_file, None)
        if type == 'vertical':
            project.push_ids(base_file)

        if dynamic_trainer_path and type == 'horizontal':
            project.upload_file(dynamic_trainer_path)

        return project

    def get_project(self, project_key: str):
        if not project_key:
            raise Exception('project_key cannot be empty or none')
        return _Project(key=project_key, api=self.project_api).get_info()

    def get_projects(self):
        return self.project_api.get_projects()

    def get_datasources(self):
        return self.datasource_api.get_datasources()

    def is_datasource_labeled(self, project_key=None, datasource_key=None):
        '''
        Accepts a valid project_key and datasource_key.
        Returns True if the datasource is labeled for the project; False otherwise

        '''
        if not datasource_key or not project_key:
            raise Exception(
                'project_key and datasource_key cannot be empty or None')

        try:
            bridge = self.project_api.get_bridge_of_project_and_datasource(
                project_key, datasource_key)

            if len(bridge['data']) == 0:
                raise Exception(
                    'datasource_key not associated with this project')

            return bridge['data'][0].get('isLabelled', True)

        except Exception as e:
            print('Something went wrong: {}'.format(e))


def get_federated_path(project_key, base, ext, ds, round):
    return f'{base}/federated_model_{project_key}_{ds}_{round}.{ext}'


def get_trained_path(project_key, base, ext, ds, round):
    return f'{base}/trained_model_{project_key}_{ds}_{round}.{ext}'
