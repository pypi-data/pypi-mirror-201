"""
This script automatically checks for changes in Operators and updates AWS infrastructure accordingly:
- Updates ECR Images
- Updates Airflow custom Operators modules

refs:
- https://towardsaws.com/build-push-docker-image-to-aws-ecr-using-github-actions-8396888a8f9e
"""
from pathlib import Path
import hashlib
import json
import os
import importlib
import boto3
import base64
import docker


def run_this():
    AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
    ecr_client = boto3.client('ecr', region_name=AWS_REGION)

    # token = ecr_client.get_authorization_token()
    # username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    # registry = token['authorizationData'][0]['proxyEndpoint']

    # docker_client = docker.from_env(version='1.24')
    # docker_client.login(username, password, registry=registry)


    here = Path()
    all_dockerfiles = {
        d.name:[] 
        for d in here.iterdir() if d.name.startswith("Dockerfile")
    }

    # Loops through Operators directories and stores relevant information in dictionary
    for d in here.iterdir():
        if d.is_dir() and not any([d.name.startswith("."), d.name.startswith("_")]):
            
            # Import Operator module
            mod = importlib.import_module(f"{d.name}.piece_function")

            all_dockerfiles[mod.dockerfile].append({
                "name": mod.name,
                "version": mod.version,
                "function_path": f"./{mod.name}/piece_function.py",
                "dockerfile": mod.dockerfile
            })


def build_and_deploy_images(all_dockerfiles):
    # Loop through all Dockerfiles to be used
    for dc, operators in all_dockerfiles:
        # We generate the name of the Image based on two parts:
        # 1. Dockerfile name: let us know which Operators run on that Conatiner
        # 2. a hash of the list of operators details copied to that Image: let us know if any Operator version has changed
        # Image name example: Dockefilebase-da53ea8b83ef008c222cc790798bc5fd3ed12063ccc53d51130534b180631d87 
        string = json.dumps(operators)
        image_name = hashlib.sha256(string.encode()).hexdigest()

        # TODO - check if Image based on this Dockerfile definition already exists

        # Loop through Operators
        for op in operators:
            # TODO - if Image doesn't exist, build and 
            cmd = ["docker", "build", "-f", f"{op['dockerfile']}", "--build-arg", f"FUNCTION_PATH={op['function_path']}", "."]

            # TODO - compare versions (hash in the name) with deployed Image, to see if it needs update


    return None
