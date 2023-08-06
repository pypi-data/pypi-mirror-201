import os
import time
from enum import Enum
from functools import wraps
from typing import List, Optional

from dagster_cloud_cli import gql
from dagster_cloud_cli.types import (
    CliEventTags,
    CliEventType,
)
from dagster_cloud_cli.ui import ExitWithMessage


def get_source() -> CliEventTags.source:
    default = CliEventTags.source.cli
    unknown = CliEventTags.source.unknown
    env_map = {
        "BITBUCKET_BUILD_NUMBER": CliEventTags.source.bitbucket,  # https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/
        "BUILDKITE": CliEventTags.source.buildkite,  # https://buildkite.com/docs/pipelines/environment-variables
        "CIRCLECI": CliEventTags.source.circle_ci,  # https://circleci.com/docs/variables/#built-in-environment-variables
        "CODEBUILD_BUILD_ID": CliEventTags.source.codebuild,  # https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html
        "GITHUB_ACTION": CliEventTags.source.github,  # https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
        "GITLAB_CI": CliEventTags.source.gitlab,  # https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
        "JENKINS_URL": CliEventTags.source.jenkins,  # https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#using-environment-variables
        "TRAVIS": CliEventTags.source.travis,  # https://docs.travis-ci.com/user/environment-variables/#default-environment-variables
    }

    sources = [value for key, value in env_map.items() if os.getenv(key)]
    if len(sources) > 1:
        return unknown
    elif sources:
        return sources[0]
    else:
        return default


def instrument(event_type: CliEventType, tags: Optional[List[Enum]] = None):
    str_tags = [str(tag.value) for tag in tags or []]
    str_tags.append(str(get_source().value))

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = kwargs.get("url")
            api_token = kwargs.get("api_token")
            start_time = time.time()

            with gql.graphql_client_from_url(
                url=str(url), token=str(api_token), retries=0
            ) as client:
                try:
                    result = func(*args, **kwargs)
                    gql.mark_cli_event(
                        client=client,
                        event_type=event_type,
                        duration_seconds=time.time() - start_time,
                        success=True,
                        tags=str_tags,
                    )
                    return result
                except ExitWithMessage as ex:
                    gql.mark_cli_event(
                        client=client,
                        event_type=event_type,
                        duration_seconds=time.time() - start_time,
                        success=False,
                        tags=str_tags,
                        message=ex.message,
                    )
                    raise

                except Exception:
                    gql.mark_cli_event(
                        client=client,
                        event_type=event_type,
                        duration_seconds=time.time() - start_time,
                        success=False,
                        tags=str_tags,
                        message="unexpected error",
                    )
                    raise

        return wrapper

    return decorator
