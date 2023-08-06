"""State module for managing ServiceAccountKeys."""
from typing import Any
from typing import Dict

__contracts__ = ["resource"]
RESOURCE_TYPE_FULL = "gcp.iam.projects.service_accounts.key"


async def present(hub, ctx, name: str):
    """Present operation is not supported for this resource.

    Args:
        name(str):
            Idem name.

    Returns:
        .. code-block:: json

            {
                "result": False,
                "comment": "...",
            }

    """
    return {
        "result": False,
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": [
            hub.tool.gcp.comment_utils.no_resource_create_update_comment(
                RESOURCE_TYPE_FULL
            )
        ],
    }


async def absent(hub, ctx, name: str):
    """Absent operation is not supported for this resource.

    Args:
        name(str):
            Idem name.

    Returns:
        .. code-block:: json

            {
                "result": False,
                "comment": "...",
                "old_state": None,
                "new_state": None,
            }

    """
    return {
        "result": False,
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": [
            hub.tool.gcp.comment_utils.no_resource_create_update_comment(
                RESOURCE_TYPE_FULL
            )
        ],
    }


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieve the list of available keys for a given service account.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.iam.projects.service_accounts.key service_account_id=...
    """
    result = {}

    list_accounts_ret = await hub.exec.gcp.iam.projects.service_account.list(
        ctx, project=ctx.acct.project_id
    )

    if not list_accounts_ret["result"]:
        hub.log.debug(
            f"Could not describe {RESOURCE_TYPE_FULL} {list_accounts_ret['comment']}"
        )
        return result

    for resource in list_accounts_ret["ret"]:
        sa_resource_id = resource.get("resource_id")

        key_ret = await hub.exec.gcp.iam.projects.service_accounts.key.list(
            ctx, project=ctx.acct.project_id, sa_resource_id=sa_resource_id
        )

        if not key_ret["result"]:
            hub.log.debug(
                f"Could not describe {RESOURCE_TYPE_FULL} in {sa_resource_id}: {key_ret['comment']}"
            )
        else:
            for service_account_key in key_ret["ret"]:
                resource_id = service_account_key.get("resource_id")
                result[resource_id] = {
                    "gcp.iam.projects.service_accounts.key.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in service_account_key.items()
                    ]
                }

    return result
