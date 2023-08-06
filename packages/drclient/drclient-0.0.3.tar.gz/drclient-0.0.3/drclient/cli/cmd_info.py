import json
from typing import Optional

import typer

from ..registry import DockerRegistryClient
from ..view.info import print_image_info


def info(
    image_name: str = typer.Argument(..., help="The name of the image"),
    output_format: Optional[str] = typer.Option(
        None, "-o", "--output-format", help="Ouput format [json]"
    ),
):
    """
    Show information for an image stored in a docker registry
    """
    registry, repository, tag = DockerRegistryClient.parse_image_url(image_name)
    drc = DockerRegistryClient(registry)
    drc.authenticate()
    manifest = drc.get_manifest(repository, tag, expand_config=True)
    if output_format == "json":
        print(json.dumps(manifest, indent=4))
    else:
        print_image_info(manifest)
