from drclient.registry.registry import DockerRegistryClient


def test_registry():
    registry, image, tag = DockerRegistryClient.parse_image_url("ubuntu")
    assert (registry, image, tag) == (
        "registry-1.docker.io",
        "library/ubuntu",
        "latest",
    )
    registry, image, tag = DockerRegistryClient.parse_image_url("python:3.10")
    assert (registry, image, tag) == ("registry-1.docker.io", "library/python", "3.10")
