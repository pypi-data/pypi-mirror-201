import re
from typing import Any
from typing import Dict

import openapi3.object_base
import tqdm

__func_alias__ = {"type_": "type"}


def plugins(hub, ctx, api: openapi3.OpenAPI) -> Dict[str, Any]:
    ret = {}
    paths: openapi3.object_base.Map = api.paths
    for name, path in tqdm.tqdm(paths.items(), desc="Parsing paths"):
        if not isinstance(path, openapi3.paths.Path):
            # Let's not fail but continue to other paths instead
            hub.log.warning(
                f"The {name} is not an instance of Path. It will not be parsed."
            )
            continue

        # Get the request type that works for this request
        for request_type in path.raw_element.keys():
            func: openapi3.paths.Operation = getattr(path, request_type)
            if not func:
                continue
            subs = [hub.tool.format.case.snake(sub) for sub in func.tags]
            if not subs:
                plugin = "init"
            else:
                plugin = subs.pop()

            refs = [ctx.service_name] + subs + [plugin]
            ref = ".".join(refs)
            if ref not in ret:
                # This is the first time we have looked at this plugin
                ret[ref] = {
                    "functions": {},
                    "doc": "",
                    "imports": [
                        "from typing import *",
                        "import dict_tools.differ as differ",
                    ],
                }

            # See if this function will be reserved CRUD operations, if so change the name
            known_func_name = None

            # e.g. /pets
            if name.endswith(plugin):
                # list/post
                if request_type == "get":
                    known_func_name = "list"
                elif request_type == "post":
                    known_func_name = "create"
            # e.g.: /pets/{id}
            elif re.match(".*(id})$", name.lower()) and name.rsplit("/", 1)[0].endswith(
                plugin
            ):
                # get/list/put
                if request_type == "get":
                    known_func_name = "get"
                elif request_type == "put" or request_type == "patch":
                    known_func_name = "update"
                elif request_type == "delete":
                    known_func_name = "delete"

            func_name = (
                hub.pop_create.openapi3.parse.resolve_function_name(name, func)
                if not known_func_name
                else known_func_name
            )
            func_data = hub.pop_create.openapi3.parse.function(func, api)
            func_data["hardcoded"] = {
                "method": request_type,
                "path": name.split(" ")[0],
                "service_name": ctx.service_name,
                "resource_name": plugin,
            }
            ret[ref]["functions"][func_name] = func_data

    return ret


def function(
    hub,
    func: openapi3.paths.Operation,
    api: openapi3.OpenAPI,
) -> Dict[str, Any]:

    params = {}
    for p in func.parameters:
        # TODO: openapi3.general.Reference is unsupported at the moment
        if isinstance(p, openapi3.paths.Parameter):
            params[p.name] = hub.pop_create.openapi3.parse.parameter(p)

    return {
        "doc": f"{func.summary}\n    {func.description}".strip(),
        "params": params,
    }


def parameter(hub, parameter: openapi3.paths.Parameter):
    if parameter.in_ == "query":
        target_type = "mapping"
    elif parameter.in_ == "path":
        target_type = "mapping"
    elif parameter.in_ == "header":
        target_type = "mapping"
    elif parameter.in_ == "cookie":
        target_type = "mapping"
    else:
        raise ValueError(f"Unknown parameter type: {parameter.in_}")

    return {
        "required": parameter.required,
        "target_type": target_type,
        "target": parameter.in_,
        "param_type": hub.pop_create.openapi3.parse.type(
            parameter.schema.type
            if isinstance(parameter.schema, openapi3.schemas.Schema)
            else None
        ),
        "doc": parameter.description or parameter.name,
    }


def type_(hub, param_type: str) -> str:
    if "integer" == param_type:
        return "int"
    elif "boolean" == param_type:
        return "bool"
    elif "number" == param_type:
        return "float"
    elif "string" == param_type:
        return "str"
    else:
        return ""


def resolve_function_name(hub, name: str, func: openapi3.paths.Operation):
    # This is the preferred way to get a function name
    func_name = func.operationId

    # Fallback function name based on the pets example
    if not func_name and " " in name:
        func_name = "_".join(name.split(" ")[1:]).lower()

    if not func_name and func.extensions:
        func_name = func.extensions[sorted(func.extensions.keys())[0]]

    if not func_name:
        func_name = func.summary

    # Maybe we need more fallbacks, you tell me
    if not func_name:
        # Maybe a fallback based on the path and method?
        raise AttributeError(f"Not sure how to find func name for {name}, help me out")

    return hub.tool.format.case.snake(func_name)
