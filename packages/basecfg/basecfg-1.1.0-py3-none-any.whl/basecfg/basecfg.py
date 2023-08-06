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
        self,
        json_config_path: Optional[str] = None,
        json_required=False,
        cli_args: Optional[Sequence[str]] = None,
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
            for key, val in self._parse_json_config(
                json_config_path, json_required
            ).items():
                setattr(self, key, val)
        for key, val in self._parse_envvars().items():
            setattr(self, key, val)
        for key, val in self._parse_args(cli_args).items():
            if val is not None:
                setattr(self, key, val)

    def _parse_json_config(self, path: str, required: bool = False) -> Dict[str, Any]:
        """parses the configuration from the json file at the given path"""
        result: Dict[str, Any] = {}
        if not os.path.isfile(path):
            if required:
                raise RuntimeError(f"required json config file {path} was not found")
            # no file, not required
            return result
        with open(path, "rt", encoding="utf8") as json_fp:
            for key, val in json.load(json_fp).items():
                if key not in self._options:
                    # in the future we may want to optionally raise an
                    # exception here
                    continue
                option = self._options[key]
                option_type = self._base_type(option.option_type)

                # check json value types against the supported types
                val_type = type(val).__name__

                coercions: Dict[str, Callable[[Any], Any]] = {
                    "bool": bool,
                    "float": float,
                    "int": int,
                    "str": str,
                    "List[bool]": self._bool_list,
                    "List[float]": self._float_list,
                    "List[int]": self._int_list,
                    "List[str]": self._str_list,
                }

                coerced_value = val
                if val_type != option_type:
                    if val_type == "list":
                        if option_type not in coercions:
                            raise TypeError(
                                f"{key}: unsupported list type {option_type}"
                            )
                    if option_type not in coercions:
                        raise TypeError(f"{key}: unsupported value type {option_type}")
                    try:
                        coerced_value = coercions[option_type](val)
                    except ValueError:
                        raise TypeError(
                            f"{key}: unsupported value type {val_type}"
                        ) from None

                if option.choices:
                    if coerced_value not in option.choices:
                        raise ValueError(
                            f'{key}: value "{coerced_value}" not in specified '
                            f"option choices ({str(option.choices)})"
                        )
                result[key] = coerced_value

        return result

    def _bool_list(self, input_list: List[Any]) -> List[bool]:
        """converts a list of unknown type into a list of bool values"""
        return [bool(x) for x in input_list]

    def _float_list(self, input_list: List[Any]) -> List[float]:
        """converts a list of unknown type into a list of float values"""
        return [float(x) for x in input_list]

    def _int_list(self, input_list: List[Any]) -> List[int]:
        """converts a list of unknown type into a list of int values"""
        return [int(x) for x in input_list]

    def _str_list(self, input_list: List[Any]) -> List[str]:
        """converts a list of unknown type into a list of str values"""
        return [str(x) for x in input_list]

    def _keys(self) -> Sequence[str]:
        """return a list of keys in this configuration"""
        return [key for key in self._options if not key.startswith("_")]

    def _parse_args(self, cli_args: Optional[Sequence[str]] = None) -> Dict[str, Any]:
        """generate an args parser and call it"""
        argp = argparse.ArgumentParser()
        for optname, option in self._options.items():
            arg_name = "--" + optname.replace("_", "-")
            option_type = self._base_type(option.option_type)

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
                arg_config["type"] = self._parse_bool

            argp.add_argument(
                arg_name,
                dest=optname,
                help=option.doc + f" (default {str(option.default)})",
                required=False,
                choices=option.choices,
                **arg_config,
            )

        return vars(argp.parse_args(args=cli_args))

    def _parse_envvars(self) -> Dict[str, Any]:
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

            coerced_value: Any = envvar_value
            option_type = self._base_type(option.option_type)
            if option_type == "str":
                coerced_value = envvar_value
            elif option_type == "bool":
                coerced_value = self._parse_bool(envvar_value)
            elif option_type == "int":
                coerced_value = int(envvar_value)
            elif option_type == "float":
                coerced_value = float(envvar_value)
            elif option_type == "List[str]":
                coerced_value = envvar_value.split(option.sep)
            elif option_type == "List[int]":
                coerced_value = [int(n) for n in envvar_value.split(option.sep)]
            elif option_type == "List[float]":
                coerced_value = [float(f) for f in envvar_value.split(option.sep)]
            elif option_type == "List[bool]":
                coerced_value = [
                    self._parse_bool(s) for s in envvar_value.split(option.sep)
                ]
            else:
                raise ValueError(
                    f"Don't know how to parse type {option.option_type} "
                    f"({option_type})"
                )
            if option.choices:
                if coerced_value not in option.choices:
                    raise ValueError(
                        f"{optname} (envvar: {envvar_name}): "
                        f'value "{coerced_value}" not in specified '
                        f"choices list ({str(option.choices)})"
                    )
            result[optname] = coerced_value
        return result

    def _base_type(self, type_spec: Any) -> str:
        """returns a string representing the type of object"""
        # print(
        #     f"spec: {type_spec}; "
        #     f"name: {type_spec.__name__}; "
        #     f"origin: {get_origin(type_spec)}; "
        #     f"args: {get_args(type_spec)}"
        # )
        result = (
            type_spec.__name__ if hasattr(type_spec, "__name__") else repr(type_spec)
        )
        origin = get_origin(type_spec)
        args = get_args(type_spec)
        if origin == Union and len(args) == 2 and args[1] == type(None):  # noqa
            # Optional[thing] where thing is in args[0]
            return self._base_type(args[0])
        if origin == list and len(args) == 1:
            if args[0] in (str, int, float, bool):
                result = f"List[{args[0].__name__}]"

        # print(f"result is: {result}")
        return result

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """evaluates the string value in a boolean context and returns the result"""
        return value.lower().strip() in ("1", "enable", "on", "true", "t", "y", "yes")
