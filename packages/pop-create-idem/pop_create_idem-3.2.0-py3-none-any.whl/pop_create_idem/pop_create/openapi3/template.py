GET_REQUEST_FORMAT = """
    result = dict(comment=[], ret=None, result=True)

    # TODO: Change function methods params if needed
    get = hub.tool.{{ function.hardcoded.service_name }}.session.request(
        ctx,
        method="{{ function.hardcoded.method }}",
        path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
            **{{ parameter.mapping.path|default({}) }}
        ),
        query_params={{ parameter.mapping.query|default({}) }},
        data={{ parameter.mapping.header|default({}) }}
    )

    if not get["result"]:
        # Send empty result for not found
        if err.status == 404:
            result["comment"].append(f"Get '{name}' result is empty")
            return result

        result["comment"].append(get["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get["ret"]:
        result["comment"].append(
            f"Get '{name}' result is empty"
        )
        return result

    result["ret"] = get["ret"]
    return result
"""

LIST_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    # TODO: Change function methods params if needed
    list = hub.tool.{{ function.hardcoded.service_name }}.session.request(
        ctx,
        method="{{ function.hardcoded.method }}",
        path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}",
        query_params={{ parameter.mapping.query|default({}) }},
        data={{ parameter.mapping.header|default({}) }}
    )

    if not list["result"]:
        result["comment"].append(list["comment"])
        result["result"] = False
        return result

    for resource in list["ret"]:
        result["ret"].append(resource)
    return result
"""

CREATE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    # TODO: Change function methods params if needed.
    create = hub.tool.{{ function.hardcoded.service_name }}.session.request(
        ctx,
        method="{{ function.hardcoded.method }}",
        path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}",
        query_params={{ parameter.mapping.query|default({}) }},
        data={{ parameter.mapping.header|default({}) }}
    )

    if not create["result"]:
        result["comment"].append(create["comment"])
        result["result"] = False
        return result

    result["comment"].append(f"Created {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)

    result["ret"] = create
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
        update = hub.tool.{{ function.hardcoded.service_name }}.session.request(
            ctx,
            method="{{ function.hardcoded.method }}",
            path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
                **{{ parameter.mapping.path|default({}) }}
            ),
            query_params={{ parameter.mapping.query|default({}) }},
            data={{ parameter.mapping.header|default({}) }}
        )

        if not create["result"]:
            result["comment"].append(update["comment"])
            result["result"] = False
            return result

        result["ret"] = update
        result["comment"].append(f"Updated {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)

    return result
"""

DELETE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    delete = hub.tool.{{ function.hardcoded.service_name }}.session.request(
        ctx,
        method="{{ function.hardcoded.method }}",
        path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
            **{{ parameter.mapping.path|default({}) }}
        ),
        query_params={{ parameter.mapping.query|default({}) }},
        data={{ parameter.mapping.header|default({}) }}
    )

    if not delete["result"]:
        result["comment"].append(delete["comment"])
        result["result"] = False
        return result

    result["comment"].append(f"Deleted '{name}'")
    return result
"""

OTHER_FUNCTION_REQUEST_FORMAT = """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.tool.{{ function.hardcoded.service_name }}.session.request(
        ctx,
        method="{{ function.hardcoded.method }}",
        path=ctx.acct.endpoint_url + "{{ function.hardcoded.path }}".format(
            **{{ parameter.mapping.path|default({}) }}
        ),
        query_params={{ parameter.mapping.query|default({}) }},
        data={{ parameter.mapping.header|default({}) }}
    )

    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result

    result["ret"] = ret
    return result
"""

PRESENT_REQUEST_FORMAT = """
    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    desired_state = {"name": name, "resource_id": resource_id, **kwargs}

    if resource_id:
        # Possible parameters: **{{ parameter.mapping.kwargs|default({}) }}
        before = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(f"'{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}:{name}' already exists")

        # If there are changes in desired state from existing state
        changes = differ.deep_diff(before.ret if before.ret else {}, desired_state)

        if bool(changes.get("new")):
            if ctx.test:
                result["new_state"] = hub.tool.{{ function.hardcoded.service_name }}.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state=desired_state
                )
                result["comment"] = (f"Would update {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **kwargs,
                    # TODO: Add other required parameters (including tags, if necessary): **{{ parameter.mapping.kwargs|default({}) }}
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(f"Updated '{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}:{name}'")
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.{{ function.hardcoded.service_name }}.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state=desired_state
            )
            result["comment"] = (f"Would create {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} {name}",)
            return result
        else:
            create_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.create(
                ctx,
                name=name,
                resource_id=resource_id,
                **kwargs
                # TODO: Add other required parameters from: **{{ parameter.mapping.kwargs|default({})}}
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(f"Created '{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}:{name}'")
                resource_id = create_ret["ret"]["resource_id"]
                # Safeguard for any future errors so that the resource_id is saved in the ESM
                result["new_state"] = dict(name=name, resource_id=resource_id)
            else:
                result["comment"].append(create_ret["comment"])

    if not result["result"]:
        # If there is any failure in create/update, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = dict(name=name, resource_id=resource_id)

    # Possible parameters: **{{ parameter.mapping.kwargs|default({}) }}
    after = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    result["new_state"] = after.ret
    return result
"""

ABSENT_REQUEST_FORMAT = """
    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if not resource_id:
        result["comment"].append(f"'{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}:{name}' already absent")
        return result

    # Remove resource_id from kwargs to avoid duplicate argument
    before = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"Would delete {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}:{name}"
            return result

        delete_ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(f"Deleted '{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}:{name}'")
        else:
            # If there is any failure in create/update, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(f"'{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}:{name}' already absent")
        return result

    result["old_state"] = before.ret
    return result
"""

DESCRIBE_REQUEST_FORMAT = """
    result = {}

    # TODO: Add other required parameters from: {{ parameter.mapping.kwargs|default({}) }}
    ret = await hub.exec.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }}.list(
        ctx
    )

    if not ret or not ret["result"]:
        hub.log.debug(f"Could not describe {{ function.hardcoded.service_name }}.{{ function.hardcoded.resource_name }} {ret['comment']}")
        return result

    for resource in ret["ret"]:
        # TODO: Look for respective identifier in **{{ function.hardcoded.resource_attributes }}
        resource_id = resource.get("TODO: Replace with resource identifier")
        result[resource_id] = {
            "{{ function.hardcoded.resource_name }}.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
"""
