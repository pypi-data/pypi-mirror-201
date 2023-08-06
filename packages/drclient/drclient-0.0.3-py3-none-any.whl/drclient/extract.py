""" This module provides functions to extract contents from docker images """
import tarfile
from pathlib import Path

tarfile.os.mknod = (
    lambda x, y, z: 0
)  # Monkey patch mknod because some layers include devices


def extract_layers(layers: dict, directory: Path):
    """Extract the contents of the layers in the given directory to a tar.gz file"""

    for layer in layers:
        layer_path = Path(directory, layer["digest"].replace(":", "_") + ".tar.gz")
        with tarfile.open(layer_path, "r:gz") as tar:
            tar.extractall(directory)
        layer_path.unlink()
