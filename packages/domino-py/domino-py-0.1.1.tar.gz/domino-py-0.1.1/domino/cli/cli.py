from rich.console import Console
from pathlib import Path
import click
import os
import uuid

from domino.cli.utils import pieces_repository, platform
import ast

console = Console()

# Ref: https://patorjk.com/software/taag/
# Font: standard
msg = """
==============================================
  ____                  _             
 |  _ \  ___  _ __ ___ (_)_ __   ___  
 | | | |/ _ \| '_ ` _ \| | '_ \ / _ \ 
 | |_| | (_) | | | | | | | | | | (_) |
 |____/ \___/|_| |_| |_|_|_| |_|\___/       
  
=============================================="""


###############################################################################
# FLOWUI PLATFORM
###############################################################################

def validate_github_token_workflows(value):
    if value and value.startswith("ghp_"):
        return value
    return None


def validate_github_token_operators(value):
    if value and value.startswith("ghp_"):
        return value
    return None


def get_cluster_name_from_env():
    cluster_name = os.environ.get("DOMINO_KIND_CLUSTER_NAME", None)
    if not cluster_name:
        cluster_name = "domino-cluster"
    return cluster_name


def get_github_workflows_ssh_private_key_from_env():
    return os.environ.get("DOMINO_GITHUB_WORKFLOWS_SSH_PRIVATE_KEY", "")

def get_github_token_pieces_from_env():
    return os.environ.get("DOMINO_GITHUB_ACCESS_TOKEN_PIECES", None)

def get_github_token_workflows_from_env():
    return os.environ.get("DOMINO_GITHUB_ACCESS_TOKEN_WORKFLOWS", None)

def get_dockerhub_username_from_env():
    return os.environ.get("DOCKERHUB_USERNAME", "")

def get_dockerhub_password_from_env():
    return os.environ.get("DOCKERHUB_PASSWORD", "")

def get_workflows_repository_from_env():
    return os.environ.get("DOMINO_WORKFLOWS_REPOSITORY", None)

def get_local_operators_repository_path():
    return ""

@click.command()
@click.option(
    '--cluster-name', 
    prompt='Local cluster name', 
    default=get_cluster_name_from_env,
    help='Define the name for the local k8s cluster.'
)
@click.option(
    '--workflows-repository',
    prompt='Workflows repository',
    default=get_workflows_repository_from_env,
    help='Github repository where the Domino workflows will be stored.'
)
@click.option(
    '--github-workflows-ssh-private-key', 
    prompt='Github ssh private for Workflows repository. If none, it will create a ssh key pair to be used.',
    default=get_github_workflows_ssh_private_key_from_env,
    help='Github ssh key for GitSync read/write operations on Workflows repository. The private key will be used in the Domino cluster and the public key should be added to the Github repository deploy keys.'
)
@click.option(
    '--github-pieces-token', 
    prompt='Github token for Pieces repository',
    default=get_github_token_pieces_from_env,
    help='Github token for read operations on Pieces repositories.'
)
@click.option(
    '--github-workflows-token', 
    prompt='Github token for Workflows Repository',
    default=get_github_token_workflows_from_env,
    help='Github token for read/write operations on Workflows Repository.'
)
@click.option(
    '--dev-mode',
    prompt='Development mode',
    default="local",
    help='Development mode - either "local" or "remote". If local it will allow you to use hot reloading for local operators repositories'
)
@click.option(
    '--local-pieces-repository-path',
    prompt='Local pieces repository path. Example: ["/path/to/repo1", "/path/to/"repo2"]',
    default=[],
    help='List of local pieces repository paths. It is used only if dev-mode is set to "local" and it will allow you to use hot reloading for local operators repositories. Example: ["path/to/repo1", "path/to/"repo2"]',
)
@click.option(
    "--local-domino-path",
    prompt="Local Domino path",
    default="",
    help="Local Domino path. It is used only if dev-mode is set to 'local' and it will allow you to use hot reloading for local Domino.",
)
def cli_prepare_platform(
    cluster_name,
    workflows_repository,
    github_workflows_ssh_private_key,
    github_pieces_token,
    github_workflows_token,
    dev_mode,
    local_pieces_repository_path,
    local_domino_path
):
    """Prepare local folder for running a Domino platform."""
    platform.prepare_platform(
        cluster_name=cluster_name, 
        workflows_repository=workflows_repository,
        github_workflows_ssh_private_key=github_workflows_ssh_private_key, 
        github_pieces_token=github_pieces_token,
        github_workflows_token=github_workflows_token,
        dev_mode=dev_mode,
        local_pieces_repository_path=ast.literal_eval(local_pieces_repository_path),
        local_domino_path=local_domino_path
    )


@click.command()
@click.option(
    "--domino-frontend-image", 
    default=None,
    help="Load a local Domino frontend image to cluster."
)
@click.option(
    "--domino-backend-image", 
    default=None,
    help="Load a local Domino backend image to cluster."
)
@click.option(
    "--run-airflow", 
    default=True,
    help="Run Domino Airflow services."
)
@click.option(
    "--use-gpu",
    is_flag=True,
    # Nvidia operator plugin reference: https://catalog.ngc.nvidia.com/orgs/nvidia/containers/gpu-operator
    help="Allow the platform to use GPUs. It will install NVIDIA plugins.",
    default=False
)
def cli_create_platform(domino_frontend_image, domino_backend_image, run_airflow, use_gpu):
    """Create cluster, install services and run Domino platform."""
    platform.create_platform(domino_frontend_image, domino_backend_image, run_airflow, use_gpu)


@click.group()
@click.pass_context
def cli_platform(ctx):
    """Domino platform actions"""
    if ctx.invoked_subcommand == "prepare":
        console.print("Let's get you started configuring a local Domino platform:")
    elif ctx.invoked_subcommand == "create":
        console.print("Your local Domino platform is being created. This might take a while...")    


cli_platform.add_command(cli_prepare_platform, name="prepare")
cli_platform.add_command(cli_create_platform, name="create")

###############################################################################
# OPERATORS REPOSITORY 
###############################################################################

def generate_random_repo_name():
    return f"new_repository_{str(uuid.uuid4())[0:8]}"


@click.command()
@click.option(
    '--name', 
    prompt="Repository's name",
    default=generate_random_repo_name,
    help="Repository's name"
)
@click.option(
    '--dockerhub-registry', 
    prompt="Dockerhub registry name",
    default="",
    help="Dockerhub registry name"
)
def cli_create_piece_repository(name, dockerhub_registry):
    """Create a basic Pieces repository with placeholder files."""
    pieces_repository.create_pieces_repository(repository_name=name, dockerhub_registry=dockerhub_registry)


@click.command()
@click.option(
    '--build-images', 
    is_flag=True,
    prompt='Build Docker images?',
    expose_value=True,
    default=False,
    help='If True (default), builds Docker images.'
)
@click.option(
    '--publish-images', 
    is_flag=True,
    prompt='Publish Docker images?',
    expose_value=True,
    default=False,
    help='If True (default), publishes Docker images to Dockerhub.'
)
@click.option(
    '--dockerhub-username', 
    prompt='Dockerhub username',
    default=get_dockerhub_username_from_env,
    help='Your username from DockerHub account.'
)
@click.option(
    '--dockerhub-password', 
    prompt='Dockerhub password',
    default=get_dockerhub_password_from_env,
    help='Your password from DockerHub account.'
)
def cli_organize_pieces_repository(build_images, publish_images, dockerhub_username, dockerhub_password):
    """Prepare local folder for running a Domino platform."""
    os.environ['DOCKERHUB_USERNAME'] = dockerhub_username
    os.environ['DOCKERHUB_PASSWORD'] = dockerhub_password
    pieces_repository.organize_pieces_repository(build_images, publish_images)


@click.command()
def cli_create_release():
    """
    Get release version for the Pieces repository in github stdout format.
    Used by github actions to set the release version.
    Needs the following env vars:
        - GITHUB_TOKEN
        - GITHUB_REPOSITORY
    """
    pieces_repository.create_release()
    

@click.group()
@click.pass_context
def cli_piece(ctx):
    """Pieces repository actions"""
    if ctx.invoked_subcommand == "organize":
        console.print(f"Organizing Pieces Repository at: {Path('.').resolve()}")
    elif ctx.invoked_subcommand == "create":
        pass


cli_piece.add_command(cli_organize_pieces_repository, name="organize")
cli_piece.add_command(cli_create_piece_repository, name="create")
cli_piece.add_command(cli_create_release, name="release")


###############################################################################
# PARENT GROUP
###############################################################################

@click.command()
def cli_run_piece_k8s():
    """Run Piece on Kubernetes Pod"""
    from domino.scripts.run_piece_k8s import run_piece as run_piece_in_k8s
    
    console.print("Running Piece inside K8s pod...")
    run_piece_in_k8s()


@click.command()
def cli_run_piece_bash():
    """Run Piece on bash"""
    from domino.scripts.run_piece_bash import run_piece as run_piece_in_bash

    console.print("Running bash Piece...")
    run_piece_in_bash()


###############################################################################
# PARENT GROUP
###############################################################################

@click.group()
@click.pass_context
def cli(ctx):
    console.print(msg, style="rgb(109,125,176)", highlight=False)
    console.print("Welcome to Domino! :red_heart-emoji:")
    console.print("")


cli.add_command(cli_platform, name="platform")
cli.add_command(cli_piece, name="piece")
cli.add_command(cli_run_piece_k8s, name="run-piece-k8s")
cli.add_command(cli_run_piece_bash, name="run-piece-bash")


if __name__ == '__main__':
    cli()
