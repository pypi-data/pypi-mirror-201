import json
import pathlib
import inspect
import pydantic
from typing import Union, Type, cast
from dataclasses import is_dataclass, asdict
from pydantic.dataclasses import dataclass as pydantic_dataclass
from .exceptions import ArgumentRequiredError, ArgumentError, RequestSchemaValidationError
from .storage import Storage
from . import envs

PydanticModel = Union[Type[pydantic.BaseModel], Type["Dataclass"]]


class BaseArgument(object):
    def __init__(self, key, alias=None, required=False, default=None, arg_spec: inspect.FullArgSpec = None, **kwargs):
        self.key = key
        self.alias = alias
        self.required = required
        self.default = default
        self.annotation = kwargs.pop("annotation", str)
        if arg_spec:
            self._init_from_arg_spec(arg_spec)

    def _init_from_arg_spec(self, arg_spec: inspect.FullArgSpec):
        if self.key not in arg_spec.args:
            return

        index = arg_spec.args.index(self.key)
        rev_index = index - len(arg_spec.args)
        if arg_spec.defaults:
            if abs(rev_index) <= len(arg_spec.defaults):
                self.default = arg_spec.defaults[rev_index]

        self.annotation = arg_spec.annotations.get(self.key, str)

    def get_value_or_default(self, value):
        if value is None:
            if self.default is None and self.required:
                raise ArgumentRequiredError(f'{self.key} is required')

            return self.default
        else:
            return value

    def load(self, value):
        """parse input data and convert to user defined type"""
        return self.get_value_or_default(value)

    def save(self, value):
        """format output data to redis message"""
        return self.get_value_or_default(value)


class String(BaseArgument):
    ...


class Int(BaseArgument):
    def load(self, value):
        value = super(Int, self).load(value)
        if value is None:
            return value

        return int(value)


class Float(BaseArgument):
    def load(self, value):
        value = super(Float, self).load(value)
        if value is None:
            return value

        return float(value)


class Number(BaseArgument):
    def load(self, value):
        value = super(Number, self).load(value)
        if value is None:
            return value

        if isinstance(value, str):
            return float(value) if '.' in value else int(value)
        else:
            return value


class Bool(BaseArgument):
    def load(self, value):
        value = super(Bool, self).load(value)
        if value is None:
            return value

        if value.lower() in ("yes", "true", "t", "y"):
            return True
        elif value.lower() in ("no", "false", "f", "n"):
            return False
        else:
            raise ArgumentError(f'invalid bool string: {value}')

    def save(self, value):
        value = super(Bool, self).save(value)
        if value is None:
            return value

        return bool(value)


class Json(BaseArgument):
    def load(self, value):
        value = super(Json, self).load(value)
        if value is None:
            return value

        if isinstance(value, dict):
            return value
        else:
            return json.loads(value)

    def save(self, value):
        value = super(Json, self).save(value)
        if value is None:
            return value

        return json.dumps(value)


class Dataclass(Json):
    def _to_pydantic_model(self) -> PydanticModel:
        pydantic_model_class: PydanticModel
        if is_dataclass(self.annotation):
            pydantic_model_class = pydantic_dataclass(self.annotation)
        else:
            pydantic_model_class = cast(PydanticModel, self.annotation)
        return pydantic_model_class

    def load(self, value):
        value = super(Dataclass, self).load(value)
        if value is None:
            return value

        model_class = self._to_pydantic_model()
        try:
            model = model_class(**value)
        except (TypeError, pydantic.ValidationError) as error:
            raise RequestSchemaValidationError(error)

        return model

    def save(self, value):
        value = self.get_value_or_default(value)
        if value is None:
            return value

        data = {}
        if is_dataclass(value):
            data = asdict(value)
        elif isinstance(value, pydantic.BaseModel):
            data = value.dict()
        return json.dumps(data)


class File(BaseArgument):
    FILENAME = "file"

    def __init__(self, key, alias=None, required=False, default=None, arg_spec: inspect.FullArgSpec = None, **kwargs):
        request_id = kwargs.get('request_id')
        super().__init__(key, alias, required, default, arg_spec, **kwargs)
        self.request_id = request_id.replace("-", "") if request_id else None

    def load(self, value):
        value = super(File, self).load(value)
        if value is None:
            return value

        key = pathlib.PurePosixPath(value) / self.FILENAME
        return str(key)

    def save(self, value):
        value = super(File, self).save(value)
        if value is None:
            return value

        storage = Storage.get_instance()
        k = pathlib.PurePosixPath('studio', envs.userId, 'tmp', envs.appId, self.request_id, envs.nodeId, self.key)
        key = str(k / self.FILENAME)
        storage.upload(key, value)
        return str(k)


class Csv(File):
    FILENAME = 'data.csv'


class Excel(File):
    FILENAME = 'data.xlsx'


class Npy(File):
    FILENAME = 'data.npy'


class Image(File):
    FILENAME = 'image.png'


DEFAULT_DATA_SUBTYPE_ARGS_MAP = {
    "all": String,
    "number": Number,
    "bool": Bool,
    "string": String,
    "array": Json,
    "dyadicArray": Json,
    "json": Json,
    "file": File,
    "system": String,
    # not used now
    "int": Int,
    "float": Float,
    # "folder": Folder,
}


def init_arg_from_arg_spec(name, arg_spec):
    annotation = arg_spec.annotations.get(name)
    if inspect.isclass(annotation):
        if issubclass(annotation, (dict, list)):
            return Json
        elif issubclass(annotation, int):
            return Int
        elif issubclass(annotation, float):
            return Float
        elif issubclass(annotation, bool):
            return Bool
        elif is_dataclass(annotation) or issubclass(annotation, pydantic.BaseModel):
            return Dataclass

    if isinstance(annotation, str):
        if annotation == 'File':
            return File
        elif annotation == 'Csv':
            return Csv
        elif annotation == 'Excel':
            return Excel
        elif annotation == 'Npy':
            return Npy
        elif annotation == 'Image':
            return Image

    return String


def init_return_from_value(value, arg_spec, index):
    annotation = arg_spec.annotations.get('return')
    if isinstance(annotation, tuple):
        annotation = annotation[index]

    if annotation:
        if inspect.isclass(annotation):
            if issubclass(annotation, (dict, list)):
                return Json
            elif issubclass(annotation, int):
                return Int
            elif issubclass(annotation, float):
                return Float
            elif issubclass(annotation, bool):
                return Bool
            elif is_dataclass(annotation) or issubclass(annotation, pydantic.BaseModel):
                return Dataclass

        if annotation == 'File':
            return File
        elif annotation == 'Csv':
            return Csv
        elif annotation == 'Excel':
            return Excel
        elif annotation == 'Npy':
            return Npy
        elif annotation == 'Image':
            return Image
    else:
        if isinstance(value, (dict, list)):
            return Json
        elif isinstance(value, int):
            return Int
        elif isinstance(value, float):
            return Float
        elif isinstance(value, bool):
            return Bool
        elif is_dataclass(value) or isinstance(value, pydantic.BaseModel):
            return Dataclass
        else:
            return String

    return String


def init_params_from_arg_spec(name, arg_spec):
    annotation = arg_spec.annotations.get(name)
    if inspect.isclass(annotation):
        if is_dataclass(annotation) or issubclass(annotation, pydantic.BaseModel):
            return Dataclass

    return Json
