import json
import sys

import click

from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton_proto.auth.authorization_service_pb2 import Assignment
from tecton_proto.auth.authorization_service_pb2 import AssignRolesRequest
from tecton_proto.auth.authorization_service_pb2 import GetAssignedRolesRequest
from tecton_proto.auth.authorization_service_pb2 import GetRolesRequest
from tecton_proto.auth.authorization_service_pb2 import UnassignRolesRequest
from tecton_proto.auth.principal_pb2 import PrincipalType
from tecton_proto.auth.resource_pb2 import ResourceType
from tecton_proto.metadataservice.metadata_service_pb2 import GetUserRequest


RESOURCE_TYPES = {
    "workspace": ResourceType.RESOURCE_TYPE_WORKSPACE,
    "organization": ResourceType.RESOURCE_TYPE_ORGANIZATION,
}


def _get_role_definitions():
    request = GetRolesRequest()
    response = metadata_service.instance().GetRoles(request)
    return response.roles


@click.command("access-control", cls=TectonGroup)
def access_control():
    """Manage Access Controls"""


@access_control.command("assign-role")
@click.option("-w", "--workspace", required=False)
# we can't make the role help dynamic without making top level usage of the CLI make a network request
# since even lazy loading following https://github.com/pallets/click/pull/2348 doesn't work for help text
@click.option(
    "-r", "--role", required=True, type=str, help="Role name (e.g. admin, owner, editor, consumer, viewer, etc)"
)
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
def assign_role_command(workspace, role, user, service_account):
    """Assign a role to a principal."""
    _update_role(workspace, role, user, service_account)


@access_control.command()
@click.option("-w", "--workspace", required=False)
# we can't make the role help dynamic without making top level usage of the CLI make a network request
# since even lazy loading following https://github.com/pallets/click/pull/2348 doesn't work for help text
@click.option(
    "-r", "--role", required=True, type=str, help="Role name (e.g. admin, owner, editor, consumer, viewer, etc)"
)
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
def unassign_role(workspace, role, user, service_account):
    """Unassign a role from a principal."""
    _update_role(workspace, role, user, service_account, unassign=True)


def _update_role(workspace, role, user, service_account, unassign=False):
    role = role.lower()
    assignment = Assignment()
    principal_type, principal_id = get_principal_details(user, service_account)

    if role == "admin":
        if workspace:
            raise click.ClickException("'Admin' is a cluster-wide role. Please remove the --workspace argument.")
        resource_type = ResourceType.RESOURCE_TYPE_ORGANIZATION
    elif workspace:
        resource_type = ResourceType.RESOURCE_TYPE_WORKSPACE
        assignment.resource_id = workspace
    else:
        raise click.ClickException("Please mention a workspace name using --workspace")

    assignment.resource_type = resource_type
    assignment.principal_type = principal_type
    assignment.principal_id = principal_id

    role_defs = _get_role_definitions()

    role_def = next((r for r in role_defs if r.id == role), None)
    if role_def is None:
        raise click.ClickException(
            f"Invalid role id. Possible values are: {', '.join(r.id for r in role_defs if _is_role_assignable(r, principal_type, resource_type))}"
        )

    assignment.role = role_def.legacy_id

    try:
        if unassign:
            request = UnassignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().UnassignRoles(request)
        else:
            request = AssignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().AssignRoles(request)
        printer.safe_print("Successfully updated role.")
    except Exception as e:
        printer.safe_print(f"Failed to update role: {e}", file=sys.stderr)
        sys.exit(1)


def _is_role_assignable(role_def, principal_type, resource_type):
    return (
        principal_type in role_def.assignable_to_principal_types
        and resource_type in role_def.assignable_on_resource_types
    )


def get_roles(principal_type, principal_id, resource_type):
    request = GetAssignedRolesRequest()
    request.principal_type = principal_type
    request.principal_id = principal_id
    request.resource_type = resource_type
    response = metadata_service.instance().GetAssignedRoles(request)
    return response


def display_table(headings, ws_roles):
    table = Displayable.from_table(headings=headings, rows=ws_roles, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(headings))])
    printer.safe_print(table)


@access_control.command("get-roles")
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option(
    "-r",
    "--resource_type",
    default=None,
    type=click.Choice(RESOURCE_TYPES.keys()),
    help="Optional Resource Type to which the Principal has roles assigned.",
)
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def get_assigned_roles(user, service_account, resource_type, json_out):
    """Get the roles assigned to a principal."""
    if resource_type is not None:
        resource_type = RESOURCE_TYPES[resource_type]
    principal_type, principal_id = get_principal_details(user, service_account)

    role_defs = _get_role_definitions()

    try:
        json_output = []
        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_WORKSPACE:
            ws_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_WORKSPACE)
            ws_roles = []
            for assignment in ws_response.assignments:
                if len(assignment.roles) > 0:
                    roles = [_maybe_convert_legacy_role_id(role_defs, role) for role in assignment.roles]
                    if json_out:
                        json_output.append(
                            {"resource_type": "WORKSPACE", "workspace_name": assignment.resource_id, "roles": roles}
                        )
                    else:
                        ws_roles.append((assignment.resource_id, ", ".join(roles)))
            if not json_out:
                headings = ["Workspace", "Role"]
                display_table(headings, ws_roles)
                printer.safe_print()

        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_ORGANIZATION:
            org_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_ORGANIZATION)
            org_roles = []
            for assignment in org_response.assignments:
                if len(assignment.roles) > 0:
                    roles = [_maybe_convert_legacy_role_id(role_defs, role) for role in assignment.roles]
                    if json_out:
                        json_output.append({"resource_type": "ORGANIZATION", "roles": roles})
                    else:
                        org_roles.append((", ".join(roles),))
            if not json_out:
                headings = ["Organization Roles"]
                display_table(headings, org_roles)

        if json_out:
            printer.safe_print(json.dumps(json_output, indent=4))

    except Exception as e:
        printer.safe_print(f"Failed to Get Roles: {e}", file=sys.stderr)
        sys.exit(1)


def _maybe_convert_legacy_role_id(role_defs, id):
    role_def = next((r for r in role_defs if r.id == id or r.legacy_id == id), None)
    role_id = id if role_def is None else role_def.id
    return role_id


def get_user_id(email):
    try:
        request = GetUserRequest()
        request.email = email
        response = metadata_service.instance().GetUser(request)
        return response.user.okta_id
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles: {e}", file=sys.stderr)
        sys.exit(1)


def get_principal_details(user, service_account):
    if user and service_account:
        raise click.ClickException("Please mention a single Principal Type using one of --user or --service-account")
    if user:
        return PrincipalType.PRINCIPAL_TYPE_USER, get_user_id(user)
    elif service_account:
        return PrincipalType.PRINCIPAL_TYPE_SERVICE_ACCOUNT, service_account
    else:
        raise click.ClickException("Please mention a Principal Type using --user or --service-account")
