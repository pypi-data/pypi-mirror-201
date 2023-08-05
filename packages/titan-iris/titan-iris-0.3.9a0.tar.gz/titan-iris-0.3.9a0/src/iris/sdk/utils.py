"""
This file contains the helper functions for the Iris package
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import io
import json
import gzip
import tarfile
from pathlib import Path
from typing import Optional

import docker
import jmespath
import requests
import wget
from rich.progress import Progress
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from iris.sdk.exception import DownloadLinkExpiredError

from .conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                         Utils                                                        #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# ------------------------------  Helper Function for Iris Pull, Upload and Download   ------------------------------ #


def make_targz(local_folder_path: str):
    """
    Create a tar.gz archive of the local folder - make this deterministic / exclude timestamp info from gz header.

    Args:
        local_folder_path: The folder to be converted to a tar.gz

    Returns: A buffer containing binary of the folder as a tar.gz file

    """
    tar_buffer = io.BytesIO()
    block_size = 4096
    # Add files to a tarfile, and then by-chunk to a tar.gz file.
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tar.add(
            local_folder_path,
            arcname=".",
            filter=lambda x: None if "pytorch_model.bin" in x.name else x,
        )
        # Exclude pytorch_model.bin if present, as safetensors should be uploaded instead.
        with gzip.GzipFile(
            filename="",  # do not emit filename into the output gzip file
            mode="wb",
            fileobj=tar_buffer,
            mtime=0,
        ) as myzip:
            for chunk in iter(lambda: tar_buffer.read(block_size), b""):
                myzip.write(chunk)

            return tar_buffer


def copy_local_folder_to_image(
    container, local_folder_path: str, image_folder_path: str
) -> None:
    """Helper function to copy a local folder into a container"""
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tar.add(local_folder_path, arcname=".")
    tar_buffer.seek(0)

    # Copy the tar archive into the container
    container.put_archive(image_folder_path, tar_buffer)


def show_progress(line, progress, tasks):  # sourcery skip: avoid-builtin-shadow
    """
    Show task progress for docker pull command (red for download, green for extract)
    """
    if line["status"] == "Downloading":
        id = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        id = f'[green][Extract  {line["id"]}]'
    else:
        # skip other statuses
        return

    if id not in tasks.keys():
        tasks[id] = progress.add_task(f"{id}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[id], completed=line["progressDetail"]["current"])


def download_model(download_url: str, model_name: str, path: str = "model_storage"):
    """helper function for iris download to download model to local machine giving download url

    Args:
        download_url (str): url to download the model
        model_name (str): name of the model
        path (str, optional): path for model storage . Defaults to "model_storage".

    Raises:
        DownloadLinkExpiredError: Download link expired error
    """

    # download the tar file
    try:
        tarfile_path = wget.download(
            download_url, path
        )  # response is the path to the downloaded file
    except Exception as e:
        raise DownloadLinkExpiredError from e

    # Extract the tar file to a folder on the local file system
    with tarfile.open(tarfile_path) as tar:
        tar.extractall(path=f"model_storage/{model_name}/models")

    # delete the tar file
    Path(tarfile_path).unlink()


def pull_image(
    model_folder_path: str,
    container_name: str,
    job_tag: str,
    task_name: str,
    baseline_model_name: str,
    baseline: bool,
):
    """
    This function handles the logic of pulling the base image and creating a new image with the model files copied into it
    """
    temp_container_name = f"temp-{container_name}"

    env_var = {
        "TASK_NAME": task_name,
        "BASELINE_MODEL_NAME": baseline_model_name,
        "BASELINE": str(baseline),
    }

    tasks = {}
    with Progress() as progress:
        # docker pull the base image
        client = docker.from_env()
        resp = client.api.pull(conf_mgr.BASE_IMAGE, stream=True, decode=True)
        for line in resp:
            show_progress(line, progress, tasks)

    # Create a new temp container
    container = client.containers.create(
        image=conf_mgr.BASE_IMAGE, name=temp_container_name, environment=env_var
    )

    copy_local_folder_to_image(
        container, model_folder_path, "/usr/local/triton/models/"
    )

    # Commit the container to a new image
    container.commit(repository=container_name)

    client.images.get(container_name).tag(f"{container_name}:{job_tag}")

    # Remove the original tag
    client.images.remove(container_name)
    # Remove the temp container
    container.remove()


def dump(response, query: Optional[str] = None):
    """
    load, a response, optionally apply a query to its returned json, and then pretty print the result
    """
    content = json.loads(response.text)
    if query:
        try:
            content = jmespath.search(query, content)
        except jmespath.exceptions.ParseError as e:
            print("Error parsing response")
            raise e

    return json.dumps(
        {"status": response.status_code, "response": content},
        indent=4,
    )


def upload_from_file(tarred: io.BytesIO, dst: str):
    """Upload a file from src (a path on the filesystm) to dst
    A url to which we have permission to send the src, via PUT.

    Args:
        tarred:
        dst (str): The url of the destination

    Returns:
        Tuple[str, requests.Response]: A hash of the file, and the response from the put request.
    """
    with tqdm(
        desc=f"Uploading",
        total=tarred.getbuffer().nbytes,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as t:
        tarred.seek(0)
        reader_wrapper = CallbackIOWrapper(t.update, tarred, "read")
        response = requests.put(dst, data=reader_wrapper)
        response.raise_for_status()
        return response
