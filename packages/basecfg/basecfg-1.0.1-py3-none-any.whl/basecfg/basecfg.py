#!/usr/bin/env python3
"""
module for specifying configuration options as a class with typed members and
loading the configuration values from json config files, environment variables,
and command-line arguments
"""
import argparse
import json
import os
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

# pylint: disable=invalid-name
OptType = TypeVar("OptType")
OptParserInput = Union[str, int, float]


class OptionMetadata(NamedTuple):
    """
    OptionMetadata is a named tuple which encapsulates data captured by OptFunc
    instances
    """

    name: Optional[str]
    option_type: Optional[Any]
    default: Any
    doc: str
    required: bool
    parser: Optional[Callable[[OptParserInput], Any]]
    choices: Optional[Any]
    sep: str


class OptFunc:
    """
    OptFunc is actually a class that lets you specify important metadata for
    options in a BaseCfg
    """

    namespace: List[OptionMetadata]

    def __init__(self) -> None:
        self.namespace = []

    def __call__(
        self,
        default: OptType,
        doc: str,
        required: bool = False,
        parser: Optional[Callable[[OptParserInput], OptType]] = None,
        choices: Optional[Sequence[OptType]] = None,
        sep: str = ",",
    ) -> OptType:
        """
        opt captures data related to a BaseCfg option and returns the default
        the annotated type of the return value is determined by the type of the
        given default argument
        """
        self.namespace.append(
            OptionMetadata(None, None, default, doc, required, parser, choices, sep)
        )
        return default

    def link(self, cls: Any):
        """class decorator which injects the optfunc attr into the wrapped class"""
        cls.optfunc = self
        return cls


# Type Alias to enable various uses in BaseCfg
_OptFunc = OptFunc


class BaseCfg:
    """
    BaseCfg is a base class for typed application configurations with
    automatic support for taking configuration data from config files,
    environment variables, and command-line arguments. Users of BaseCfg
    subclass basecfg.BaseCfg and add typed class attributes, defining
    them with basecfg.opt
    """

    OptFunc = _OptFunc  # this is an alias to enable users to call BaseCfg.OptFunc()
    optfunc: _OptFunc  # this is an attribute set by OptFunc.link
    _options: Dict[str, OptionMetadata]

    def __init__(
        self, json_config_path: Optional[str] = None, json_required=False
    ) -> None:
        """parse data from various sources according to options"""
        # step 1 is to enrich our metadata about the configuration options, at
        # this point we finally have the names of the fields and are aware of
        # their resolved type annotations
        self._options = {}

        option_metadata = iter(self.optfunc.namespace)
        for key, val in self.__class__.__annotations__.items():
            self._options[key] = next(option_metadata)._replace(
                name=key, option_type=val
            )

        if json_config_path:
            for key, val in self.parse_json_config(
                json_config_path, json_required
            ).items():
                setattr(self, key, val)
        for key, val in self.parse_envvars().items():
            setattr(self, key, val)
        for key, val in self.parse_args().items():
            setattr(self, key, val)

    def parse_json_config(self, path: str, required: bool = False) -> Dict[str, Any]:
        """parses the configuration from the json file at the given path"""
        result: Dict[str, Any] = {}
        if not os.path.isfile(path):
            if required:
                raise RuntimeError(f"required json config file {path} was not found")
            # no file, not required
            return result
        with open(path, "rt", encoding="utf8") as json_fp:
            for key, val in json.load(json_fp).items():
                result[key] = val
        return result

    def parse_args(self) -> Dict[str, Any]:
        """generate an args parser and call it"""
        argp = argparse.ArgumentParser()
        for optname, option in self._options.items():
            arg_name = "--" + optname.replace("_", "-")
            option_type = self.base_type(option.option_type)

            # use this for as little as possible (because it doesn't get type checked)
            # it could be good to switch to TypedDict for this
            arg_config: Dict[str, Any] = {
                "action": "store",
            }
            if option_type == "bool":
                arg_config["action"] = argparse.BooleanOptionalAction
            elif option_type == "int":
                arg_config["type"] = int
            elif option_type == "float":
                arg_config["type"] = float
            elif option_type == "List[str]":
                arg_config["action"] = "append"
            elif option_type == "List[int]":
                arg_config["action"] = "append"
                arg_config["type"] = int
            elif option_type == "List[float]":
                arg_config["action"] = "append"
                arg_config["type"] = float
            elif option_type == "List[bool]":
                arg_config["action"] = "append"
                arg_config["type"] = self.parse_bool

            argp.add_argument(
                arg_name,
                dest=optname,
                default=option.default,
                help=option.doc,
                choices=option.choices,
                **arg_config,
            )

        return vars(argp.parse_args())

    def parse_envvars(self) -> Dict[str, Any]:
        """parse environment variables for configuration values"""
        # pylint: disable=too-many-branches
        result: Dict[str, Any] = {}

        for optname, option in self._options.items():
            envvar_name: str = optname.upper()
            envvar_value: str
            if envvar_name in os.environ:
                envvar_value = os.environ[envvar_name]
            elif optname in os.environ:
                envvar_name = optname
                envvar_value = os.environ[envvar_name]
            else:
                continue

            option_type = self.base_type(option.option_type)
            if option_type == "str":
                result[optname] = envvar_value
            if option_type == "bool":
                result[optname] = self.parse_bool(envvar_value)
            elif option_type == "int":
                result[optname] = int(envvar_value)
            elif option_type == "float":
                result[optname] = float(envvar_value)
            elif option_type == "List[str]":
                result[optname] = option.sep.split(envvar_value)
            elif option_type == "List[int]":
                result[optname] = [int(n) for n in option.sep.split(envvar_value)]
            elif option_type == "List[float]":
                result[optname] = [float(f) for f in option.sep.split(envvar_value)]
            elif option_type == "List[bool]":
                result[optname] = [
                    self.parse_bool(s) for s in option.sep.split(envvar_value)
                ]
            else:
                raise ValueError(
                    f"Don't know how to parse type {option.option_type} "
                    f"({option_type})"
                )
        return result

    def base_type(self, type_spec: Any) -> str:
        """returns a string representing the type of object"""
        print(
            f"spec: {type_spec}; "
            f"name: {type_spec.__name__}; "
            f"origin: {get_origin(type_spec)}; "
            f"args: {get_args(type_spec)}"
        )
        result = (
            type_spec.__name__ if hasattr(type_spec, "__name__") else repr(type_spec)
        )
        origin = get_origin(type_spec)
        args = get_args(type_spec)
        if origin == Union and len(args) == 2 and args[1] == type(None):  # noqa
            # Optional[thing] where thing is in args[0]
            return self.base_type(args[0])
        if origin == list and len(args) == 1:
            if args[0] in (str, int, float, bool):
                result = f"List[{args[0].__name__}]"

        print(f"result is: {result}")
        return result

    @staticmethod
    def parse_bool(value: str) -> bool:
        """evaluates the string value in a boolean context and returns the result"""
        return value.lower().strip() in ("1", "enable", "on", "true", "t", "y", "yes")
