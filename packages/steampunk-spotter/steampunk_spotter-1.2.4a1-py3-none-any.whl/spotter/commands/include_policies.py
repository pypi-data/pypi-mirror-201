"""Provide include-policies CLI command."""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from spotter.api import ApiClient
from spotter.storage import Storage


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new parser for include-policies command to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "include-policies", help="Include custom policies",
        description="Include custom OPA policies written in Rego Language"
    )
    project_organization_group = parser.add_mutually_exclusive_group()
    project_organization_group.add_argument(
        "--project-id", "-p", type=str, help="UUID of an existing Steampunk Spotter project to apply custom policies "
                                             "to."
    )
    project_organization_group.add_argument(
        "--organization-id", type=str, help="UUID of an existing Steampunk Spotter organization to apply custom "
                                            "policies to."
    )
    parser.add_argument(
        "path", type=lambda p: Path(p).absolute(),
        help="Path to the file or folder with custom OPA policies written in Rego Language"
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    """
    Execute callback for include-policies command.

    :param args: Argparse arguments
    """
    api_endpoint = args.endpoint or os.environ.get("SPOTTER_ENDPOINT", None)
    storage_path = args.storage_path or Storage.DEFAULT_PATH
    api_token = args.api_token or os.environ.get("SPOTTER_API_TOKEN")
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")

    path: Path = args.path
    if not path.exists():
        print(f"Error: Path at {path} provided for scanning does not exist.", file=sys.stderr)
        sys.exit(2)
    if not path.is_file() and not path.is_dir():
        print(f"Error: Path at {path} is not a file or directory.", file=sys.stderr)
        sys.exit(2)

    include_policies(
        api_endpoint, storage_path, api_token, username, password, args.project_id, args.organization_id, path
    )


# pylint: disable=too-many-arguments,too-many-locals
def include_policies(api_endpoint: Optional[str], storage_path: Path, api_token: Optional[str], username: Optional[str],
                     password: Optional[str], project_id: Optional[str], organization_id: Optional[str],
                     path: Path) -> None:
    """
    Suggest module and task examples by calling Spotter's AI component.

    :param api_endpoint: Steampunk Spotter API endpoint
    :param storage_path: Path to storage
    :param api_token: Steampunk Spotter API token
    :param username: Steampunk Spotter username
    :param password: Steampunk Spotter password
    :param project_id: UUID of an existing Steampunk Spotter project to apply custom policies to
    :param organization_id: UUID of an existing Steampunk Spotter organization to apply custom policies to
    :param path: Path to the folder with custom OPA policies
    :return: List of suggestions
    """
    storage = Storage(storage_path)

    # TODO: extract this to a separate configuration component along with other configuration file options
    if api_endpoint is None:
        if storage.exists("spotter.json"):
            storage_configuration_json = storage.read_json("spotter.json")
            endpoint = storage_configuration_json.get("endpoint", ApiClient.DEFAULT_ENDPOINT)
        else:
            endpoint = ApiClient.DEFAULT_ENDPOINT
    else:
        endpoint = api_endpoint

    policies: List[Dict[str, Any]] = []
    if path.is_file():
        item = {
            "policy_name": path.name,
            "policy_rego": path.read_text(),
            "severity": "",
            "description": "",
            "type": "CUSTOM"
        }
        policies.append(item)
    else:
        for task_file in path.rglob("*.rego"):
            item = {
                "policy_name": task_file.name,
                "policy_rego": task_file.read_text(),
                "severity": "",
                "description": "",
                "type": "CUSTOM"
            }
            policies.append(item)

    payload = {
        "policies": policies,
        "project_id": project_id,
        "organization_id": organization_id
    }

    api_client = ApiClient(endpoint, storage, api_token, username, password)
    api_client.put("/v2/opa/", payload=payload)
    print("Custom policies successfully included.")
