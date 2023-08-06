import atexit
import os
import shutil
import tarfile
from pathlib import Path
from tempfile import mkdtemp

import typer

from ..extract import extract_layers
from ..registry import DockerRegistryClient
from ..threaded_pull import pull_layers_in_threads
from ..view.info import sizeof_fmt


def pull(
    image_name: str = typer.Argument(..., help="The name of the image"),
    tar_file: Path = typer.Option(
        None, "-t", "--tar-file", help="Output to a tar.gz file"
    ),
    output_directory: Path = typer.Option(
        None, "-d", "--output-directory", help="Output to a directory"
    ),
):
    """
    Pull image from a docker registry
    """
    if tar_file and output_directory:
        raise typer.BadParameter("Cannot specify both output file and output directory")

    registry, repository, tag = DockerRegistryClient.parse_image_url(image_name)
    source_reference = f"{registry}/{repository}:{tag}"

    drc = DockerRegistryClient(registry)
    drc.authenticate()
    manifest = drc.get_manifest(repository, tag)
    layers = manifest["layers"]
    local_image_name = f"{repository}:{tag}"
    total_size = sum([layer["size"] for layer in layers])
    print(
        f"Pulling {len(layers)} layer(s) [{sizeof_fmt(total_size)}] "
        f"for image {source_reference} to local image {local_image_name}"
    )

    if output_directory is None:
        output_directory = mkdtemp()
        if tar_file:
            atexit.register(shutil.rmtree, output_directory)
    else:
        if not output_directory.exists():
            output_directory.mkdir(parents=True)
        else:
            if not output_directory.is_dir():
                raise typer.BadParameter(
                    f"Output directory {output_directory} is not a directory"
                )
            os.scandir(output_directory)
            if any(os.scandir(output_directory)):
                raise typer.BadParameter(
                    f"Output directory {output_directory} is not empty"
                )

    pull_layers_in_threads(drc, layers, output_directory)
    extract_layers(layers, Path(output_directory))
    if tar_file:
        os.chdir(output_directory)
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(".", recursive=True)
        os.chdir("/")
    else:
        print(f"Contents of {source_reference} extracted to {output_directory}")
