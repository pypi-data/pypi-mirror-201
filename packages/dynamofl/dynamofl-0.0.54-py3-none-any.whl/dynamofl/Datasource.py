from dynamofl.api.DatasourceAPI import DatasourceAPI


class _Datasource:
    def __init__(self, key, type, api: DatasourceAPI):
        self._api = api
        self.key: str = key
        self.trainers = {}

        # Can be 'horizontal', 'label' or 'feature'
        self.type = type

    def add_trainer(self, key, train_callback, test_callback, default_hyper_params=None, description=None, model_path=None):
        params = {'key': key}
        if default_hyper_params is not None:
            params['defaultHyperParams'] = default_hyper_params
        if description is not None:
            params['description'] = description
        if self.type is not None and self.type != 'horizontal':
            params['type'] = self.type

        self._api.create_trainers(self.key, params=params)

        self.trainers[key] = {
            'train': train_callback,
            'test': test_callback,
        }

        if model_path is not None:
            self.trainers[key]['model_path'] = model_path

    def get_datasource(self):
        return self._api.get_datasource(key=self.key)
