"""Engine 7 / Security: Role-Based Access Control (RBAC) Enforcement."""

ROLES = {
    "operator": {"can_intake": True, "can_review": False, "can_audit": True},
    "reviewer": {"can_intake": True, "can_review": True, "can_audit": True},
    "auditor": {"can_intake": False, "can_review": False, "can_audit": True},
}


def verify_permission(role: str, action: str) -> bool:
    """Server-side permission check ensuring unauthorized roles are blocked."""
    role_perms = ROLES.get(role.lower())
    if not role_perms:
        return False
    return role_perms.get(action, False)


def enforce_rbac(role: str, action: str):
    """Raises a PermissionError if the given role cannot perform the action."""
    if not verify_permission(role, action):
        raise PermissionError(
            f"Access Denied: Role '{role}' is not authorized to perform action '{action}'."
        )