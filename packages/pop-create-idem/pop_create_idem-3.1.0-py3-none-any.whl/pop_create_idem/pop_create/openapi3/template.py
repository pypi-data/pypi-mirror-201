HTTP_REQUEST = """
    return hub.tool.{{ function.hardcoded.service_name }}.session.request(
        ctx,
        method="{{ function.hardcoded.method }}",
        path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
            **{{ parameter.mapping.path|default({}) }}
        ),
        query_params={{ parameter.mapping.query|default({}) }},
        data={{ parameter.mapping.header|default({}) }}
    )
"""

GET_REQUEST_FORMAT = """
    result = dict(comment=[], ret=None, result=True)

    # TODO: Change function methods params if needed
    try:
        get = hub.tool.{{ function.hardcoded.service_name }}.session.request(
            ctx,
            method="{{ function.hardcoded.method }}",
            path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
                **{{ parameter.mapping.path|default({}) }}
            ),
            query_params={{ parameter.mapping.query|default({}) }},
            data={{ parameter.mapping.header|default({}) }}
        )

        # Case: Empty results
        if not get:
            result["comment"].append(
                f"Get '{name}' result is empty"
            )
            return result

        result["ret"] = get
        return result
    except ClientResponseError as err:
        # Case: Error
        if err.status == 404:
            result["comment"].append(err.reason)
            return result

        result["comment"].append(err.reason)
        result["result"] = False
        return result
"""

LIST_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    # TODO: Change function methods params if needed
    try:
        list = hub.tool.{{ function.hardcoded.service_name }}.session.request(
            ctx,
            method="{{ function.hardcoded.method }}",
            path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
                **{{ parameter.mapping.path|default({}) }}
            ),
            query_params={{ parameter.mapping.query|default({}) }},
            data={{ parameter.mapping.header|default({}) }}
        )
        for resource in list:
            result["ret"].append(resource)
        return result
    except ClientResponseError as err:
        result["comment"].append(err.reason)
        result["result"] = False
        return result
"""

CREATE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    try:
        # TODO: Change function methods params if needed.
        create = hub.tool.{{ function.hardcoded.service_name }}.session.request(
            ctx,
            method="{{ function.hardcoded.method }}",
            path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
                **{{ parameter.mapping.path|default({}) }}
            ),
            query_params={{ parameter.mapping.query|default({}) }},
            data={{ parameter.mapping.header|default({}) }}
        )
        result["comment"].append(f"Created {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)

        result["ret"] = create
        return result
    except ClientResponseError as err:
        result["comment"].append(err.reason)
        result["result"] = False
        return result
"""

UPDATE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    desired_state = {"name": name, "resource_id": resource_id, **kwargs}

    resource_to_raw_input_mapping = OrderedDict(
    **{{ parameter.mapping.path|default({})|pprint|indent(12,true) }}
    )

    parameters_to_update = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            parameters_to_update[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if parameters_to_update:
        try:
            update = hub.tool.{{ function.hardcoded.service_name }}.session.request(
                ctx,
                method="{{ function.hardcoded.method }}",
                path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
                    **{{ parameter.mapping.path|default({}) }}
                ),
                query_params={{ parameter.mapping.query|default({}) }},
                data={{ parameter.mapping.header|default({}) }}
            )

            if update.status > 400:
                result["result"] = False
                result["comment"].append(update["comment"])
                return result

            result["ret"] = update
            result["comment"].append(f"Updated {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)
        except ClientResponseError as err:
            result["comment"].append(err.reason)
            result["result"] = False

    return result
"""

DELETE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    try:
        delete = hub.tool.{{ function.hardcoded.service_name }}.session.request(
            ctx,
            method="{{ function.hardcoded.method }}",
            path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
                **{{ parameter.mapping.path|default({}) }}
            ),
            query_params={{ parameter.mapping.query|default({}) }},
            data={{ parameter.mapping.header|default({}) }}
        )

        result["comment"].append(f"Deleted '{name}'")
        return result
    except ClientResponseError as err:
        result["comment"].append(err.reason)
        result["result"] = False
        return result
"""

OTHER_FUNCTION_REQUEST_FORMAT = """
    result = dict(comment=[], ret=None, result=True)

    try:
        ret = await hub.tool.{{ function.hardcoded.service_name }}.session.request(
            ctx,
            method="{{ function.hardcoded.method }}",
            path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
                **{{ parameter.mapping.path|default({}) }}
            ),
            query_params={{ parameter.mapping.query|default({}) }},
            data={{ parameter.mapping.header|default({}) }}
        )

        result["ret"] = ret
        return result
    except ClientResponseError as err:
        result["comment"].append(err.reason)
        result["result"] = False
        return result
"""

PRESENT_REQUEST_FORMAT = """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs") and v is not None
    }

    if resource_id:
        before_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

        result["old_state"] = copy.deepcopy(before_ret["ret"])
    if before:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.{{ function.hardcoded.service_name }}.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state=desired_state
            )
            result["comment"] = (f"Would update {{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)
            return result

        # TODO: Add other required parameters (including tags, if necessary)
        update_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.update(
            ctx,
            name=name,
            resource_id=resource_id,
            # TODO: Add other required parameters (including tags, if necessary): **{{ parameter.mapping.kwargs|default({}) }}
        )

        resource_updated = bool(update_ret["ret"])
        if not resource_updated:
            result["comment"].append(f"'{name}' already exists")
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result

        result["comment"].append(
            f"Updated {{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'",
        )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.{{ function.hardcoded.service_name }}.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state=desired_state
            )
            result["comment"] = (f"Would create {{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} {name}",)
            return result

        create_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.create(
            ctx,
            name=name,
            resource_id=resource_id,
            # TODO: Add other required parameters from: **{{ parameter.mapping.kwargs|default({})}}
        )
        result["result"] = create_ret["result"]
        if not result["result"]:
            result["comment"].append(create_ret["comment"])
            return result

        result["comment"].append(f"Created '{name}'")

        # TODO: extract resource_id from create_ret
        resource_id = create_ret["ret"]["TODO: extract resource_id from the response"]
        # This makes sure the created resource is saved to esm regardless if the subsequent update call fails or not.
        result["new_state"] = {"name": name, "resource_id": resource_id}
        result["comment"].append(f" Created {{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} name={name}")

    # TODO: Add other required parameters
    # Possible parameters: **{{ parameter.mapping.kwargs|default({}) }}
    after = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    result["new_state"] = after["ret"]
    return result
"""

ABSENT_REQUEST_FORMAT = """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    # This is to make absent idempotent. If absent is run again, it would be a no-op
    if not resource_id:
        result["comment"] = f"{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} name={name} already absent."
        return result

    # TODO: Add other required parameters
    # Possible parameters: **{{ parameter.mapping.kwargs|default({}) }}
    before_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    # Case: Error
    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    # Case: Not Found
    if not before_ret["ret"]:
        result["comment"] = f"{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}' already absent."
        return result

    if ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = f"Would delete {{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'"
        return result

    result["old_state"] = before_ret["ret"]

    # TODO: Add other required parameters
    # Possible parameters: **{{ parameter.mapping.kwargs|default({}) }}
    delete_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.delete(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    result["result"] = delete_ret["result"]
    if not result["result"]:
        result["comment"].append(delete_ret["comment"])
        return result

    result["comment"] = f"Deleted {{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'"
    return result
"""

DESCRIBE_REQUEST_FORMAT = """
    result = {}

    # TODO: Add other required parameters from: {{ parameter.mapping.kwargs|default({}) }}
    ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.list(
        ctx
    )

    if not ret or not ret["result"]:
        hub.log.debug(f"Could not describe {{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} {ret['comment']}")
        return result

    for resource in ret["ret"]:
        # TODO: Look for respective identifier in **{{ function.hardcoded.resource_attributes }}
        resource_id = resource.get("TODO: Replace with resource identifier")
        result[resource_id] = {
            "{{ function.hardcoded.service_name }}.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
"""
