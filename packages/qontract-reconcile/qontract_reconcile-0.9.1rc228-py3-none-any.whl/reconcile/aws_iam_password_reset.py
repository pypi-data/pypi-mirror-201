import logging
import sys
from collections.abc import (
    Iterable,
    Mapping,
)
from typing import (
    Any,
    Optional,
)

from reconcile import queries
from reconcile.utils.aws_api import AWSApi
from reconcile.utils.defer import defer
from reconcile.utils.state import init_state

QONTRACT_INTEGRATION = "aws-iam-password-reset"


def get_roles(
    roles: Iterable[Mapping[str, Any]], org_username: str
) -> Optional[Mapping[str, Any]]:
    for d in roles:
        if d["org_username"] == org_username:
            return d
    return None


def account_in_roles(roles: Iterable[Mapping[str, Any]], aws_account: str) -> bool:
    for role in roles:
        for g in role.get("aws_groups") or []:
            if g["account"]["name"] == aws_account:
                return True
    return False


@defer
def run(dry_run, defer=None):
    accounts = queries.get_aws_accounts(reset_passwords=True)
    settings = queries.get_app_interface_settings()
    roles = queries.get_roles(aws=True)
    state = init_state(integration=QONTRACT_INTEGRATION)
    defer(state.cleanup)

    for a in accounts:
        account_name = a["name"]
        reset_passwords = a.get("resetPasswords")
        if not reset_passwords:
            continue
        with AWSApi(1, [a], settings=settings) as aws_api:
            for r in reset_passwords:
                user_name = r["user"]["org_username"]
                request_id = r["requestId"]
                state_key = f"{account_name}/{user_name}/{request_id}"
                if state.exists(state_key):
                    continue

                role = get_roles(roles, user_name)
                if not role:
                    logging.error(f"Expected a role to be found with name {user_name}")
                    sys.exit(1)

                if not account_in_roles(role["roles"], account_name):
                    logging.error(f"User {user_name} is not in account {account_name}")
                    sys.exit(1)

                logging.info(["reset_password", account_name, user_name])
                if dry_run:
                    continue

                aws_api.reset_password(account_name, user_name)
                aws_api.reset_mfa(account_name, user_name)
                state.add(state_key)
