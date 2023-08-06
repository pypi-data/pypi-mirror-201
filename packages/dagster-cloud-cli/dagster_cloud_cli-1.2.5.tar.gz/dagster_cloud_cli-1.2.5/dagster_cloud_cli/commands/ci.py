# CI/CD agnostic commands that work with the current CI/CD system

import json
import logging
import os
import pathlib
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List

import pydantic
import typer
from typer import Typer

from .. import ui
from ..core import pydantic_yaml
from . import metrics

app = Typer(hidden=True, help="CI/CD agnostic commands")
from dagster_cloud_cli.core.pex_builder import code_location, github_context
from dagster_cloud_cli.types import CliEventTags


@app.command(help="Print json information about current CI/CD environment")
def inspect(project_dir: str):
    project_dir = os.path.abspath(project_dir)
    source = metrics.get_source()
    info = {"source": str(source), "project-dir": project_dir}
    if source == CliEventTags.source.github:
        info.update(load_github_info(project_dir))
    print(json.dumps(info))


def load_github_info(project_dir: str) -> Dict[str, Any]:
    event = github_context.get_github_event(project_dir)
    return {
        "git-url": event.commit_url,
        "commit-hash": event.github_sha,
    }


@app.command(
    help=(
        "Print the branch deployment name (or nothing) for the current context. Creates a new"
        " branch deployment if necessary. Requires DAGSTER_CLOUD_URL and DAGSTER_CLOUD_API_TOKEN"
        " environment variables."
    )
)
def branch_deployment(project_dir: str):
    source = metrics.get_source()
    if source == CliEventTags.source.github:
        event = github_context.get_github_event(project_dir)
        url = os.environ["DAGSTER_CLOUD_URL"]
        api_token = os.environ["DAGSTER_CLOUD_API_TOKEN"]
        deployment_name = code_location.create_or_update_branch_deployment_from_github_context(
            url, api_token, event
        )
        print(deployment_name)
    else:
        logging.error("branch-deployment not supported for %s", source)
        sys.exit(1)


def get_validation_errors(validation_error: pydantic.ValidationError) -> List[str]:
    errors = []
    for error in validation_error.errors():
        if "type" in error:
            location = ".".join([str(part) for part in error["loc"] if part != "__root__"])
            if error["type"] == "value_error.missing":
                errors.append(f"expected '{location}': missing required field")
            elif error["type"] == "value_error.extra":
                errors.append(f"unexpected '{location}': unknown field")
            else:
                errors.append(f"{error['type']} at '{location}': {error['msg']}")
    return errors


@dataclass
class CheckResult:
    errors: List[str] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)


def check_dagster_cloud_yaml(yaml_path: pathlib.Path) -> CheckResult:
    result = CheckResult()

    if not yaml_path.exists():
        result.errors.append(f"No such file {yaml_path}")
        return result

    yaml_text = yaml_path.read_text()
    if not yaml_text.strip():
        result.errors.append(f"Unexpected blank file {yaml_path}")
        return result

    try:
        parsed = pydantic_yaml.load_dagster_cloud_yaml(yaml_path.read_text())
    except pydantic.ValidationError as err:
        for error in get_validation_errors(err):
            result.errors.append(error)
        return result

    for location in parsed.locations:
        if location.build and location.build.directory:
            build_path = yaml_path.parent / location.build.directory
            if not build_path.is_dir():
                result.errors.append(
                    f"Build directory {build_path} not found for location"
                    f" {location.location_name} at {build_path.absolute()}"
                )
    return result


@app.command(help="Validate configuration")
def check(project_dir: str = typer.Option(".")):
    def passed(msg):
        ui.print("✅ " + msg)

    def failed(msg):
        raise ui.error(msg)

    project_path = pathlib.Path(project_dir)
    yaml_path = project_path / "dagster_cloud.yaml"
    result = check_dagster_cloud_yaml(yaml_path)
    if result.errors:
        for msg in result.errors:
            ui.error("[dagster_cloud.yaml] " + msg)
        failed(
            "Invalid dagster_cloud.yaml, please see"
            " https://docs.dagster.io/dagster-cloud/developing-testing/code-locations#syncing-the-workspace"
        )
    else:
        passed("dagster_cloud.yaml checked")
