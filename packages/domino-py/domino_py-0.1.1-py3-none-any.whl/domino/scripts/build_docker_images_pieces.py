from pathlib import Path
import docker
import tomli
import json
import shutil
import os
from colorama import Fore, Back, Style
from rich.console import Console

from domino.cli.utils.constants import COLOR_PALETTE


console = Console()


def build_and_publish_from_tmp_dockerfile(source_image_name: str, publish: bool):
    client = docker.from_env()
    try:
        os.environ["DOCKER_BUILDKIT"] = "1"
        print(Fore.BLUE + f"Building docker image: {source_image_name}")
        build_results = client.images.build(
            path=".",
            dockerfile="Dockerfile-tmp",
            tag=source_image_name,
            nocache=True,
            forcerm=True
        )
        print(Style.RESET_ALL + Style.DIM, end='')
        for r in build_results[1]:
            if "stream" in r and r["stream"] != "\n":
                print(r)
        print(Style.RESET_ALL + Fore.BLUE + f"Finished building: {source_image_name}")
        if publish:
            print(f"Publishing docker image: {source_image_name}")
            print(Style.RESET_ALL + Style.DIM, end='')
            try:
                dockerhub_username = os.environ.get("DOCKERHUB_USERNAME", None)
                dockerhub_password = os.environ.get("DOCKERHUB_PASSWORD", None)
                client.login(username=dockerhub_username, password=dockerhub_password)
            except docker.errors.APIError:
                console.print("Unauthorized login")
                raise
            response = client.images.push(repository=source_image_name)
            print(response, end='')
            print(Style.RESET_ALL + Fore.BLUE + f"Finished publishing: {source_image_name}")
        print(Style.RESET_ALL)
    except Exception as e:
        raise Exception(e)
    finally:
        # remove tmp dockerfile
        Path("Dockerfile-tmp").unlink()    



def build_images_from_pieces_repository(publish: bool = False):
    """
    Each dependencies group will need to have its own Docker image built and published to be used by Domino.
    This is because the Operators source code goes baked in the images.
    The only exception is if dependencies["docker_image"] =! None, in which case we presume the image was pre-built
    with all the requirements and with the Operators source code included.
    """

    dependencies_path = Path(".") / "dependencies"
    domino_path = Path(".") / ".domino"
    config_path = Path(".") / "config.toml"

    # Get information from config.toml file
    with open(config_path, "rb") as f:
        config_dict = tomli.load(f)
    docker_image_repository = config_dict.get("repository").get("REPOSITORY_NAME")
    docker_image_version = config_dict.get("repository").get("VERSION")

    if publish:
        dockerhub_registry_name = config_dict.get("dockerhub").get("REGISTRY_NAME")
    else:
        dockerhub_registry_name = "local"

    # Load dependencies_map.json file
    with open(domino_path / "dependencies_map.json", "r") as f:
        pieces_dependencies_map = json.load(f)

    # Build docker images from unique definitions
    for group, v in pieces_dependencies_map.items():
        dependency_dockerfile = v["dependency"].get("dockerfile", None)
        dependency_requirements = v["dependency"].get("requirements_file", None)
        source_image_name = f"{dockerhub_registry_name}/{docker_image_repository}:{docker_image_version}-{group}"

        # If no extra dependency, use base worker image and just copy Operators source code
        if not any([dependency_dockerfile, dependency_requirements]):
            pieces_dependencies_map[group]["source_image"] = source_image_name
            # TODO change base image to domino when we have it
            dockerfile_str = f"""FROM taufferconsulting/flowui-airflow-pod:latest
COPY config.toml domino/pieces_repository/
COPY pieces domino/pieces_repository/pieces
COPY .domino domino/pieces_repository/.domino
"""
            with open("Dockerfile-tmp", "w") as f:
                f.write(dockerfile_str)

        # If dependency is defined as a Dockerfile, copy it to root path and run build/publish
        elif dependency_dockerfile:
            pieces_dependencies_map[group]["source_image"] = source_image_name
            build_dockerfile_path = str(dependencies_path.resolve() / dependency_dockerfile)
            shutil.copyfile(build_dockerfile_path, "Dockerfile-tmp")

        # If dependency is defined as a requirements.txt
        elif dependency_requirements:
            pieces_dependencies_map[group]["source_image"] = source_image_name
            # TODO change base image to domino when we have it
            dockerfile_str = f"""FROM taufferconsulting/flowui-airflow-pod:latest
COPY config.toml domino/pieces_repository/
COPY pieces domino/pieces_repository/pieces
COPY .domino domino/pieces_repository/.domino
COPY dependencies/{dependency_requirements} domino/pieces_repository/dependencies/
RUN pip install --no-cache-dir -r domino/pieces_repository/dependencies/{dependency_requirements}
"""
# RUN source domino_env/bin/activate \
#     && pip install --no-cache-dir -r flowui/pieces_repository/dependencies/{dependency_requirements}
# """ 
            with open("Dockerfile-tmp", "w") as f:
                f.write(dockerfile_str)

        build_and_publish_from_tmp_dockerfile(
            source_image_name=source_image_name, 
            publish=publish
        )
    
    return pieces_dependencies_map