import threading
from functools import partial
from queue import Queue

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from .registry import DockerRegistryClient


def pull_layers_in_threads(drc: DockerRegistryClient, layers, output_dir: str):
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        TransferSpeedColumn(),
        DownloadColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    ) as progress:
        result_queue = Queue()
        for layer in layers:
            total = layer["size"]
            task = progress.add_task(f'Downloading...{layer["digest"]}', total=total)
            download_thread = threading.Thread(
                target=download_layer, args=(drc, layer, task, result_queue, output_dir)
            )
            download_thread.start()
        running_threads = len(layers)
        while running_threads:
            task, delta = result_queue.get()
            if delta is None:
                running_threads -= 1
            progress.update(task, advance=delta)


def download_layer(drc: DockerRegistryClient, layer, task, result_queue, output_dir):
    def update_progress(task, result_queue, item):
        result_queue.put((task, item))

    try:
        drc.get_blob(
            layer["digest"],
            output_dir,
            partial(update_progress, task, result_queue),
        )
    # Any error terminates the thread and sends a None to the result queue
    except:  # noqa: E722
        result_queue.put((task, None))
        raise

    result_queue.put((task, None))
