import copy

LIST_RESOURCES_WITH_PRESENT_WRAPPER = [
    "gcp.compute.instance",
    "gcp.compute.disk",
    "gcp.compute.forwarding_rule",
    "gcp.compute.subnetwork",
    "gcp.compute.backend_service",
    "gcp.compute.machine_image",
    "gcp.compute.instance_group",
    "gcp.compute.snapshot",
]

LIST_RESOURCES_WITH_ABSENT_WRAPPER = [
    "gcp.compute.disk",
    "gcp.compute.firewall",
    "gcp.compute.forwarding_rule",
    "gcp.compute.health_check",
    "gcp.compute.image",
    "gcp.compute.instance",
    "gcp.compute.instance_group",
    "gcp.compute.machine_image",
    "gcp.compute.network",
    "gcp.compute.node_template",
    "gcp.compute.reservation",
    "gcp.compute.resource_policy",
    "gcp.compute.snapshot",
    "gcp.compute.subnetwork",
]


async def call_present(hub, ctx):
    name = ctx.kwargs.get("name", None)
    state_ctx = ctx.kwargs.get("ctx")
    assert state_ctx, f"state context is missing: {state_ctx}"

    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    gcp_service_resource_type = state_ctx.get("tag").split("_|")[0]
    # TODO: This needs to be removed once all resources follow the contract
    if gcp_service_resource_type not in LIST_RESOURCES_WITH_PRESENT_WRAPPER:
        return await ctx.func(*ctx.args, **ctx.kwargs)

    if not ctx.kwargs.get("project"):
        ctx.kwargs["project"] = hub.tool.gcp.utils.get_project_from_account(
            state_ctx, ctx.kwargs.get("project")
        )

    service_resource_type = gcp_service_resource_type.replace("gcp.", "")
    resource_type_camel = hub.tool.gcp.case.camel(
        gcp_service_resource_type.split(".")[-1]
    )

    resource_path = service_resource_type.split(".")
    hub_ref_exec = hub.exec.gcp
    for resource_path_segment in resource_path:
        hub_ref_exec = hub_ref_exec[resource_path_segment]

    resource_id = (
        (ctx.kwargs.get("resource_id") or {})
        or (state_ctx.get("old_state") or {}).get("resource_id")
        or (state_ctx.get("rerun_data") or {}).get("resource_id")
    )
    local_params = {**ctx.kwargs}
    local_params.update({resource_type_camel: name})

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )

    if hub.tool.gcp.resource_prop_utils.properties_mismatch_resource_id(
        service_resource_type, resource_id, local_params
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                gcp_service_resource_type, name
            )
        )

    if state_ctx.get("rerun_data"):
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            state_ctx,
            state_ctx.get("rerun_data"),
            service_resource_type,
        )

        if not handle_operation_ret["result"]:
            result["comment"] += handle_operation_ret["comment"]
            if handle_operation_ret.get("rerun_data"):
                result["rerun_data"] = handle_operation_ret["rerun_data"]
                if handle_operation_ret["rerun_data"].get("has_error", False):
                    result["result"] = False
            else:
                result["result"] = False

            return result

        resource_id = handle_operation_ret["resource_id"]

    if resource_id:
        old_get_ret = await hub_ref_exec.get(state_ctx, resource_id=resource_id)

        if not old_get_ret["result"] or (
            not old_get_ret["ret"]
            and (state_ctx.get("rerun_data") or get_resource_only_with_resource_id)
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        # long-running operation has succeeded - both update and create
        if state_ctx.get("rerun_data"):
            result["new_state"] = old_get_ret["ret"]
            result["old_state"] = state_ctx.get("rerun_data").get("old_state")
            if result["old_state"]:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.update_comment(
                        gcp_service_resource_type, name
                    )
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.create_comment(
                        gcp_service_resource_type, name
                    )
                )

            ctx_kwargs = {k: v for (k, v) in ctx.kwargs.items() if v is not None}
            diff = hub.tool.gcp.utils.compare_states(
                result["new_state"], ctx_kwargs, service_resource_type
            )
            values_mismatch: set = diff.get("relevant_changes")
            if values_mismatch:
                values_mismatch.discard("root['ctx']")
                if values_mismatch:
                    result["comment"].append(
                        f"Values mismatch between actual and desired states: {values_mismatch}"
                    )
            return result

        result["old_state"] = old_get_ret["ret"]
    elif not get_resource_only_with_resource_id:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            service_resource_type, local_params
        )

        if not resource_id:
            result["result"] = False
            result["comment"].append(
                f"Could not construct resource ID of {service_resource_type} from input arguments."
            )
            return result

        old_get_ret = await hub_ref_exec.get(state_ctx, resource_id=resource_id)

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = old_get_ret["ret"]

    state_ctx["wrapper_result"] = result
    return await ctx.func(*ctx.args, **{**ctx.kwargs, "resource_id": resource_id})


async def post_present(hub, ctx):
    if ctx.ret and "old_state" in ctx.ret and "new_state" in ctx.ret:
        old_state = ctx.ret.get("old_state")
        new_state = ctx.ret.get("new_state")

        state_ctx = ctx.kwargs.get("ctx")
        resource_state_path = state_ctx.get("tag").split("_|")[0]
        service_resource_type = (
            hub.tool.gcp.resource_prop_utils.get_service_resource_type(
                resource_state_path
            )
        )

        changes = hub.tool.gcp.utils.compare_changes(
            copy.deepcopy(old_state), copy.deepcopy(new_state), service_resource_type
        )
        ctx.ret["changes"] = changes


async def call_absent(hub, ctx):
    state_ctx = ctx.kwargs.get("ctx")
    assert state_ctx, f"state context is missing: {state_ctx}"

    gcp_service_resource_type = state_ctx.get("tag").split("_|")[0]
    service_resource_type = gcp_service_resource_type.replace("gcp.", "")
    resource_type_camel = hub.tool.gcp.case.camel(
        gcp_service_resource_type.split(".")[-1]
    )

    if gcp_service_resource_type not in LIST_RESOURCES_WITH_ABSENT_WRAPPER:
        return await ctx.func(*ctx.args, **ctx.kwargs)

    name = ctx.kwargs.get("name", None)

    result = {
        "comment": [],
        "old_state": state_ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "result": True,
    }

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )

    resource_id = ctx.kwargs.get("resource_id")

    if not resource_id and not get_resource_only_with_resource_id:
        project = hub.tool.gcp.utils.get_project_from_account(
            state_ctx, ctx.kwargs.get("project")
        )
        zone = ctx.kwargs.get("zone")
        region = ctx.kwargs.get("region")
        resource_id = (state_ctx.get("old_state") or {}).get(
            "resource_id"
        ) or hub.tool.gcp.resource_prop_utils.construct_resource_id(
            service_resource_type,
            {
                **locals(),
                resource_type_camel: name,
            },
        )

    if not resource_id and not state_ctx.get("rerun_data"):
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(
                gcp_service_resource_type, name
            )
        )
        return result

    if not state_ctx.get("rerun_data"):
        resource_path = service_resource_type.split(".")
        hub_ref_exec = hub.exec.gcp
        for resource_path_segment in resource_path:
            hub_ref_exec = hub_ref_exec[resource_path_segment]

        get_ret = await hub_ref_exec.get(state_ctx, resource_id=resource_id)

        if not get_ret["result"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        if not get_ret["ret"]:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.already_absent_comment(
                    gcp_service_resource_type, name
                )
            )
            return result

        result["old_state"] = get_ret["ret"]
    else:
        result["old_state"] = state_ctx["rerun_data"]["old_state"]

    name = result["old_state"].get("name", name)

    if state_ctx.get("test"):
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(
                gcp_service_resource_type, name
            )
        )
        return result

    if not state_ctx.get("rerun_data"):
        hub_ref_exec_gcp_api = hub.exec.gcp_api.client
        for resource_path_segment in resource_path:
            hub_ref_exec_gcp_api = hub_ref_exec_gcp_api[resource_path_segment]

        # First iteration; invoke resource's delete()
        delete_ret = await hub_ref_exec_gcp_api.delete(
            state_ctx, resource_id=resource_id, request_id=ctx.kwargs.get("request_id")
        )

        if not delete_ret.get(
            "result"
        ) or not hub.tool.gcp.operation_utils.is_operation(delete_ret.get("ret")):
            result["result"] = False
            result["comment"].append(
                f"Unexpected return value from {service_resource_type}.delete - {delete_ret}"
            )
            return result

        result["result"] = True
        result["comment"] += delete_ret["comment"]
        operation_id = delete_ret["ret"].get("selfLink")
        result["rerun_data"] = {
            "operation_id": hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation_id,
                hub.tool.gcp.operation_utils.get_operation_type(operation_id),
            ),
            "old_state": result["old_state"],
        }
        return result
    else:
        # delete() has been called on some previous iteration
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, state_ctx.get("rerun_data"), service_resource_type
        )
        if not handle_operation_ret["result"]:
            result["comment"] += handle_operation_ret["comment"]
            if handle_operation_ret.get("rerun_data"):
                result["rerun_data"] = handle_operation_ret["rerun_data"]
                if handle_operation_ret["rerun_data"].get("has_error", False):
                    result["result"] = False
            else:
                result["result"] = False

            return result

        result["comment"].append(
            hub.tool.gcp.comment_utils.delete_comment(gcp_service_resource_type, name)
        )
    return result
