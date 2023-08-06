import json
from typing import Dict, Optional, Sequence

import rich_click as click

from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.dao import application


@click.group(name="trigger", cls=GROUP_CLS)
def trigger_command():
    """
    Trigger a deployed job asynchronously
    """
    pass


@click.command(
    name="job",
    cls=COMMAND_CLS,
    context_settings=dict(ignore_unknown_options=True),
    help="Trigger a Job asynchronously",
)
@click.option(
    "--application-fqn",
    "--application_fqn",
    type=click.STRING,
    required=True,
    help="FQN of the deployment of the Job. This can be found on the Job details page.",
)
@click.option("--command", type=click.STRING, required=False, help="Command to run")
@click.option(
    "--params",
    type=click.UNPROCESSED,
    required=False,
    help="Parameters to pass to the job",
)
@handle_exception_wrapper
def trigger_job(
    application_fqn: str,
    command: Optional[Sequence[str]],
    params: Optional[Dict[str, str]],
):
    if params:
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            raise Exception("Invalid JSON passed for `params`")
    application.trigger_job(
        application_fqn=application_fqn, command=command, params=params
    )


def get_trigger_command():
    trigger_command.add_command(trigger_job)
    return trigger_command
