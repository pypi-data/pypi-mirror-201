import requests
import functools
import inspect
import json

class Vectorshift():
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def transformation(self,
                       name: str,
                       inputs: dict,
                       outputs: dict,
                       description: str = 'No description',
                       type: str = 'Custom',
                       can_output: bool = True,
                       takes_context: bool = False,
                       override: bool = False):
        def transformation_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                function_str = inspect.getsource(func)
                function_str = function_str[function_str.find('\ndef ')+1:]
                transformation_params = {
                    'name': name,
                    'description': description,
                    'type': type,
                    'inputs': inputs,
                    'outputs': outputs,
                    'function': function_str,
                    'functionName': func.__name__,
                    'canOutput': can_output,
                    'takesContext': takes_context,
                    'override': override
                }
                requests.post('https://api.vector-shift.com/api/transformations/user/create',
                              data={'transformation': json.dumps(transformation_params), 'api_key': self.api_key})
                return func(*args, **kwargs)
            return wrapper
        return transformation_decorator

    def add_transformation(self,
                           func,
                           name: str,
                           inputs: dict,
                           outputs: dict,
                           description: str = 'No description',
                           type: str = 'Custom',
                           can_output: bool = True,
                           takes_context: bool = False,
                           override: bool = False):
        function_str = inspect.getsource(func)
        function_str = function_str[function_str.find('\ndef ')+1:]
        transformation_params = {
            'name': name,
            'description': description,
            'type': type,
            'inputs': inputs,
            'outputs': outputs,
            'function': function_str,
            'functionName': func.__name__,
            'canOutput': can_output,
            'takesContext': takes_context,
            'override': override
        }
        return requests.post('https://api.vector-shift.com/api/transformations/user/create',
                             data={'transformation': json.dumps(transformation_params), 'api_key': self.api_key})

    def run_transformation(self,
                           id: str = '',
                           name: str = '',
                           inputs: dict = {}):
        query_dict = {'id': id, 'name': name}
        query_params = f'''?{'&'.join([f'{k}={v}' for k, v in query_dict.items() if v != ''])}'''
        response = requests.post(f'https://api.vector-shift.com/api/transformations/user/run{query_params}',
                             data={'inputs': json.dumps(inputs), 'api_key': self.api_key}).text
        return json.loads(response)

    def get_source_info(self,
                        id: str = '',
                        name: str = ''):
        query_dict = {'id': id, 'name': name}
        query_params = f'''?{'&'.join([f'{k}={v}' for k, v in query_dict.items() if v != ''])}'''
        response = requests.get(f'https://api.vector-shift.com/api/sources/info{query_params}',
                            data={'api_key': self.api_key}).text
        return json.loads(response)

    def get_transformation_info(self,
                                id: str = '',
                                name: str = '',
                                scope='user'):
        query_dict = {'id': id, 'name': name}
        query_params = f'''?{'&'.join([f'{k}={v}' for k, v in query_dict.items() if v != ''])}'''
        response = requests.get(f'https://api.vector-shift.com/api/transformations/{scope}/info{query_params}',
                            data={'api_key': self.api_key}).text
        return json.loads(response)
