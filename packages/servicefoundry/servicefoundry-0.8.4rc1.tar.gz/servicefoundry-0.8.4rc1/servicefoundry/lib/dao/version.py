from typing import Optional

from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)


def list_versions(
    application_fqn: str,
    client: Optional[ServiceFoundryServiceClient] = None,
):
    client = client or ServiceFoundryServiceClient()
    application = client.get_id_from_fqn(fqn=application_fqn, fqn_type="app")
    versions = client.list_versions(application_id=application["applicationId"])
    return versions


def get_version(
    application_fqn: str,
    version: int,
    client: Optional[ServiceFoundryServiceClient] = None,
):
    client = client or ServiceFoundryServiceClient()
    application = client.get_id_from_fqn(fqn=application_fqn, fqn_type="app")
    versions = client.list_versions(
        application_id=application["applicationId"], deployment_version=version
    )
    if len(versions) == 0:
        raise ValueError(
            f"Version {version!r} for Application with FQN {application_fqn!r} does not exist."
        )
    return versions[0]
