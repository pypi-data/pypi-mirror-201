"""Exec module for managing ServiceAccountKeys."""
from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, sa_resource_id: str, project: str = None):
    r"""Lists every ServiceAccountKey that belongs to a specific project.

    Args:
        sa_resource_id(str):
            Resource id of the service account following the pattern projects/{project}/serviceAccounts/{id}.
        project(str, Optional):
            The resource name of the project associated with the service accounts.
    """
    execution_context = ExecutionContext(
        resource_type="iam.projects.service_accounts.key",
        method_name="list",
        method_params={"ctx": ctx, "name": sa_resource_id},
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    project: str = None,
    service_account_id: str = None,
    key_id: str = None,
    resource_id: str = None,
):
    r"""Returns the specified ServiceAccountKey resource.

    Args:
        project(str, Optional):
            Project ID for this request.
        service_account_id(str, Optional):
            Email or unique_id of the service account in GCP.
        key_id(str, Optional):
            Id of the service account key in GCP.
        resource_id(str, Optional):
            An identifier of the service account key in idem. Defaults to None.
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    if service_account_id and key_id:
        project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
        resource_id = (
            f"projects/{project}/serviceAccounts/{service_account_id}/keys/{key_id}"
        )
    elif not resource_id:
        result["result"] = False
        result["comment"] = [
            f"gcp.iam.projects.service_accounts.key#get(): either service_account_id and key_id or resource_id"
            f" should be specified."
        ]
        return result

    execution_context = ExecutionContext(
        resource_type="iam.projects.service_accounts.key",
        method_name="get",
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result
