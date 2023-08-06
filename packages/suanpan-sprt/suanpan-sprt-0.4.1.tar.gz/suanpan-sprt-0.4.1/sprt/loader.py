import json
import logging
import inspect
import pathlib
import importlib
import importlib.util
from .arguments import init_arg_from_arg_spec, init_return_from_value, DEFAULT_DATA_SUBTYPE_ARGS_MAP
from .storage import Storage
from .exceptions import ParamsArgError
from . import envs


class NodeFunction(object):
    def __init__(self, node_id, working_dir, filename, function='main'):
        file = pathlib.Path(filename)
        self.name = file.stem
        self.location = pathlib.Path(working_dir) / filename
        self.function = function
        self.module = self.load_module()
        self.context = RuntimeContext(envs.userId, envs.appId, node_id)

    def load_module(self):
        if not self.location.is_file():
            raise Exception(f'invalid component file: {self.location}')

        spec = importlib.util.spec_from_file_location(self.name, self.location)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    async def call_func(self, request_id, args, params):
        in_slot = []
        has_context = False

        func = getattr(self.module, self.function)
        arg_spec = inspect.getfullargspec(func)
        for index, a in enumerate(arg_spec.args):
            if a == 'context':
                if index != len(arg_spec.args) - 1:
                    raise ParamsArgError('context MUST be the last argument of function')

                has_context = True
                continue

            arg_class = init_arg_from_arg_spec(a, arg_spec)
            arg = arg_class(a, arg_spec=arg_spec)

            inx = f'in{index + 1}'
            value = args.get(inx)
            value = arg.load(value)

            in_slot.append(value)

        self.context.reset(request_id, params)
        if has_context or arg_spec.varkw is not None:
            if inspect.iscoroutinefunction(func):
                ret = await func(*in_slot, context=self.context)
            else:
                ret = func(*in_slot, context=self.context)
        else:
            raise ParamsArgError('function MUST have a "context" argument')

        if isinstance(ret, tuple):
            return {f'out{index + 1}': init_return_from_value(r, arg_spec, index)(
                f'out{index + 1}', request_id=request_id).save(r)
                    for index, r in enumerate(ret)}
        else:
            return {'out1': init_return_from_value(ret, arg_spec, 0)(f'out{1}', request_id=request_id).save(ret)}


class RuntimeContext(object):
    def __init__(self, user_id, app_id, node_id):
        self.request_id = None
        self.user_id = user_id
        self.app_id = app_id
        self.node_id = node_id
        self.params = NodeParams()
        self.log = logging.getLogger('logkit')
        self.storage = Storage.get_instance()

    def reset(self, request_id, params):
        self.request_id = request_id
        if not isinstance(params, dict):
            params = json.loads(params)
        self.params._data = params

    def __repr__(self):
        return f'<Context: request_id {self.request_id}>'


class NodeParams(object):
    def __init__(self):
        self._data = {}

    def meta(self, name):
        return self._data.get(name)

    def __getattr__(self, name):
        param = self.meta(name)
        if not param:
            return param

        _type = param.get('type')
        _value = param.get('value')

        arg_class = DEFAULT_DATA_SUBTYPE_ARGS_MAP.get(_type)
        return arg_class(name).load(_value)

    def __getitem__(self, item):
        return self.__getattr__(item)
