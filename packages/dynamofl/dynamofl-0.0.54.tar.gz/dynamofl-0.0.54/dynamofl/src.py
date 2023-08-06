from .Helpers import Helpers
from .MessageHandler import _MessageHandler
from .State import _State

RETRY_AFTER = 5  # seconds


class DynamoFL():
    def __init__(self, token: str, host: str = 'https://api.dynamofl.com', metadata: object = None):
        self._state = _State(token, host, metadata)

        self._messagehandler = _MessageHandler(self._state)
        self._messagehandler.connect_to_ws()

    def attach_datasource(self, key, name=None, metadata=None, type=None):
        return self._state.attach_datasource(key, name, metadata, type)

    def delete_datasource(self, key):
        return self._state.delete_datasource(key)

    def get_datasources(self):
        return self._state.get_datasources()

    def delete_project(self, key):
        return self._state.delete_project(key)

    def get_user(self):
        return self._state.get_user()

    def create_project(self, base_model_path, params, dynamic_trainer_path=None, type='horizontal'):
        return self._state.create_project(base_model_path, params, dynamic_trainer_path, type)

    def get_project(self, project_key):
        return self._state.get_project(project_key)

    def get_projects(self):
        return self._state.get_projects()

    def is_datasource_labeled(self, project_key=None, datasource_key=None):
        '''
        Accepts a valid datasource_key and project_key
        Returns True if the datasource is labeled for the project; False otherwise

        '''
        return self._state.is_datasource_labeled(project_key=project_key, datasource_key=datasource_key)
