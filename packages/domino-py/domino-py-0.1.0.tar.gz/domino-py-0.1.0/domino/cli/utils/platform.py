import os
import tomli
import tomli_w
import yaml
import subprocess
from pathlib import Path
from rich.console import Console

from domino.cli.utils.constants import COLOR_PALETTE #,DOMINO_HELM_PATH
from yaml.resolver import BaseResolver

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import base64
import domino.helm as domino_helm
from tempfile import NamedTemporaryFile
from kubernetes import client, config


class AsLiteral(str):
  pass

def represent_literal(dumper, data):
  return dumper.represent_scalar(BaseResolver.DEFAULT_SCALAR_TAG, data, style="|")

yaml.add_representer(AsLiteral, represent_literal)


console = Console()

def create_ssh_pair_key() -> None:
    # Create SSH key pair for GitHub Workflows
    console.print("Generating SSH key pair for GitHub Workflows...")
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=4096
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return private_key, public_key
    

def prepare_platform(
    cluster_name: str, 
    workflows_repository: str, 
    github_workflows_ssh_private_key: str, 
    github_pieces_token: str, 
    github_workflows_token: str,
    dev_mode: str,
    local_pieces_repository_path: list,
    local_domino_path: str
) -> None:
    # Create local configuration file updated with user-provided arguments
    config_file_path = Path(__file__).resolve().parent / "config-domino-local.toml"
    with open(str(config_file_path), "rb") as f:
        config_dict = tomli.load(f)
    
    running_path = str(Path().cwd().resolve())
    config_dict["path"]["DOMINO_LOCAL_RUNNING_PATH"] = running_path
    config_dict["kind"]["DOMINO_KIND_CLUSTER_NAME"] = cluster_name
    config_dict['kind']['dev_mode'] = dev_mode

    config_dict['local_pieces_repositories'] = {}
    config_dict['local_domino_repository'] = {"DOMINO_LOCAL_DOMINO_REPOSITORY": ""}
    if dev_mode == 'local':
        config_dict['local_domino_repository']['DOMINO_LOCAL_DOMINO_REPOSITORY'] = local_domino_path
        for local_pieces_repository in local_pieces_repository_path:
            # Read repo config.toml to get repo name to map it to cluster path
            repo_config_file_path = Path(local_pieces_repository).resolve() / "config.toml"
            with open(str(repo_config_file_path), "rb") as f:
                repo_toml = tomli.load(f)
            
            repo_name = repo_toml['repository']['REPOSITORY_NAME'] 
            config_dict['local_pieces_repositories'][repo_name] = local_pieces_repository

    config_dict['github']['DOMINO_GITHUB_WORKFLOWS_REPOSITORY'] = workflows_repository.split("github.com/")[-1].strip('/')

    if not github_workflows_ssh_private_key:
        private_key, public_key = create_ssh_pair_key()
        config_dict["github"]["DOMINO_GITHUB_WORKFLOWS_SSH_PRIVATE_KEY"] = base64.b64encode(private_key).decode('utf-8')
        config_dict["github"]["DOMINO_GITHUB_WORKFLOWS_SSH_PUBLIC_KEY"] = public_key.decode("utf-8")
    else:
        config_dict["github"]["DOMINO_GITHUB_WORKFLOWS_SSH_PRIVATE_KEY"] = github_workflows_ssh_private_key

    config_dict["github"]["DOMINO_GITHUB_ACCESS_TOKEN_PIECES"] = github_pieces_token
    config_dict['github']['DOMINO_GITHUB_ACCESS_TOKEN_WORKFLOWS'] = github_workflows_token
    
    with open("config-domino-local.toml", "wb") as f:
        tomli_w.dump(config_dict, f)

    console.print("")
    console.print(f"Domino is prepared to run at: {running_path}")
    console.print(f"You can check and modify the configuration file at: {running_path}/config-domino-local.toml")
    console.print("Next, run: `domino platform create`")
    console.print("")


def create_platform(domino_frontend_image: str = None, domino_backend_image: str = None, run_airflow: bool = True, use_gpu: bool = False) -> None:
    # Load configuration values
    with open("config-domino-local.toml", "rb") as f:
        platform_config = tomli.load(f)

    # Create kind config file and run bash script to create Kind cluster
    kubeadm_config_patches = dict(
        kind="InitConfiguration",
        nodeRegistration=dict(
            kubeletExtraArgs={
                "node-labels": "ingress-ready=true"
            }
        )
    )
    extra_mounts_local_repositories = []
    if platform_config['kind']['dev_mode'] == 'local':
        for repo_name, repo_path in platform_config['local_pieces_repositories'].items():
            extra_mounts_local_repositories.append(
                dict(
                    hostPath=repo_path,
                    containerPath=f"/pieces_repositories/{repo_name}",
                    readOnly=True,
                    propagation='HostToContainer'
                )
            )
        if platform_config['local_domino_repository'].get('DOMINO_LOCAL_DOMINO_REPOSITORY'):
            extra_mounts_local_repositories.append(
                dict(
                    hostPath=platform_config['local_domino_repository']['DOMINO_LOCAL_DOMINO_REPOSITORY'],
                    containerPath=f"/domino_dev", # TODO change in next build
                    readOnly=True,
                    propagation='HostToContainer'
                )
            )

    kubeadm_parsed = AsLiteral(yaml.dump(kubeadm_config_patches))
    use_gpu_dict = {} if not use_gpu else {"gpus": True}
    kind_config = dict(
        kind="Cluster",
        apiVersion="kind.x-k8s.io/v1alpha4",
        nodes=[
            dict(
                role="control-plane",
                kubeadmConfigPatches=[kubeadm_parsed],
                extraPortMappings=[
                    dict(
                        containerPort=80,
                        hostPort=80,
                        listenAddress="0.0.0.0",
                        protocol="TCP"
                    ),
                    dict(
                        containerPort=443,
                        hostPort=443,
                        listenAddress="0.0.0.0",
                        protocol="TCP"
                    )
                ]
            ),
            dict(
                role="worker",
                extraMounts=[
                    dict(
                        hostPath=platform_config["path"]["DOMINO_LOCAL_RUNNING_PATH"] + "/workflow_shared_storage",
                        containerPath="/cluster_shared_storage",
                        readOnly=False,
                        propagation="Bidirectional"
                    ),
                    *extra_mounts_local_repositories
                ],
                **use_gpu_dict
            ),
        ]
    )
    with open("kind-cluster-config.yaml", "w") as f:
        yaml.dump(kind_config, f)

    cluster_name = platform_config["kind"]["DOMINO_KIND_CLUSTER_NAME"]
    
    # Open helm values file and update with user-provided arguments
    domino_helms_path = Path(os.path.dirname(domino_helm.__file__))
    domino_base_helm_path = domino_helms_path / 'domino-base'
    domino_airlflow_helm_path = domino_helms_path / 'domino-airflow'

    console.print(f"Removing previous Kind cluster - {cluster_name}...")
    subprocess.run(["kind", "delete", "cluster", "--name", cluster_name])
    console.print(f"Creating new Kind cluster - {cluster_name}...")
    subprocess.run(["kind", "create", "cluster", "--name", cluster_name, "--config", "kind-cluster-config.yaml"])
    console.print("")
    console.print("Kind cluster created successfully!", style=f"bold {COLOR_PALETTE.get('success')}")

    # TODO - Install services with helm upgrade
    console.print("")
    console.print("Installing NGINX controller...")
    subprocess.run(["kubectl", "apply", "-f", "https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml"], stdout=subprocess.DEVNULL)
    subprocess.run(["kubectl", "wait", "--namespace", "ingress-nginx", "--for", "condition=ready", "pod", "--selector=app.kubernetes.io/component=controller", "--timeout=180s"])

    if domino_frontend_image:
        console.print(f"Loading local frontend image {domino_frontend_image} to Kind cluster...")
        subprocess.run(["kind", "load", "docker-image", domino_frontend_image , "--name", cluster_name, "--nodes", f"{cluster_name}-worker"])
    else:
        domino_frontend_image = "taufferconsulting/flowui-frontend:latest" # TODO change to domino image name
    
    if domino_backend_image:
        console.print(f"Loading local backend image {domino_backend_image} to Kind cluster...")
        subprocess.run(["kind", "load", "docker-image", domino_backend_image , "--name", cluster_name, "--nodes", f"{cluster_name}-worker"])
    else:  
        domino_backend_image = "taufferconsulting/flowui-backend:latest" # TODO change to domino image name

    """
    In order to use nvidia gpu in our cluster we need nvidia plugins to be installed.
    We can use nvidia operator to install nvidia plugins.

    References: 
        https://catalog.ngc.nvidia.com/orgs/nvidia/containers/gpu-operator
        https://jacobtomlinson.dev/posts/2022/quick-hack-adding-gpu-support-to-kind/
    """
    if use_gpu:
        console.print("Installing NVIDIA GPU Operator...")
        nvidia_gpu_operator_add_repo_command = [
            "helm", "repo", "add", "nvidia", "https://nvidia.github.io/gpu-operator",
        ]
        subprocess.run(nvidia_gpu_operator_add_repo_command)
        helm_update_command = ["helm", "repo", "update"]
        subprocess.run(helm_update_command)

        # We don't need driver as we are using kind and our host machine already has nvidia driver that is why we are disabling it.
        nvidia_plugis_install_command = "helm install --wait --generate-name -n gpu-operator --create-namespace nvidia/gpu-operator --set driver.enabled=false"
        subprocess.run(nvidia_plugis_install_command, shell=True)

    token_pieces = platform_config["github"]["DOMINO_GITHUB_ACCESS_TOKEN_PIECES"]
    token_workflows = platform_config["github"]["DOMINO_GITHUB_ACCESS_TOKEN_WORKFLOWS"]
    console.print("\nInstalling Domino services...\n")
    # Install Domino Services
    # TODO use remote helm chart
    subprocess.run([
        "helm", "install", 
        "--set", f"github_access_token_pieces={token_pieces}",
        "--set", f"github_access_token_workflows={token_workflows}",
        "--set", f"frontend.image={domino_frontend_image}",
        "--set", f"backend.image={domino_backend_image}",
        "--set", f"backend.workflowsRepository={platform_config['github']['DOMINO_GITHUB_WORKFLOWS_REPOSITORY']}",
        "domino",
        domino_base_helm_path
    ])

    if not run_airflow:
        console.print("")
        console.print("K8s resources created successfully!", style=f"bold {COLOR_PALETTE.get('success')}")

        console.print("You can now access the Domino frontend at: http://localhost/")
        console.print("and the Backend API at: http://localhost/api/")
        return
        
    console.print("\nInstalling Domino Airflow services...\n")

    console.print("\nInstalling Domino Airflow services...\n")
    # Create temporary airflow values with user provided arguments
    airflow_ssh_config = dict(
        gitSshKey=f"{platform_config['github']['DOMINO_GITHUB_WORKFLOWS_SSH_PRIVATE_KEY']}",
    )
    airflow_ssh_config_parsed = AsLiteral(yaml.dump(airflow_ssh_config))

    workers_extra_volumes = []
    workers_extra_volumes_mounts = []
    workers = {}
    scheduler = {}
    if platform_config['kind']["dev_mode"] == 'local' and platform_config['local_domino_repository'].get('DOMINO_LOCAL_DOMINO_REPOSITORY'):
        workers_extra_volumes = [
            {
                "name": "domino-dev-extra",
                "persistentVolumeClaim": {
                    "claimName": "domino-dev-volume-claim"
                }
            }
        ]
        workers_extra_volumes_mounts = [
            {
                "name": "domino-dev-extra",
                "mountPath": "/opt/airflow/domino_dev" # TODO change to /domino_dev
            }
        ]
        workers = {
            "workers": {
                "extraVolumes": workers_extra_volumes,
                "extraVolumeMounts": workers_extra_volumes_mounts,
            }
        }
        scheduler = {
            "scheduler": {
                "extraVolumes": workers_extra_volumes,
                "extraVolumeMounts": workers_extra_volumes_mounts,
            }
        }

    airflow_values_override_config = {
        "airflow": {
            "enabled": True,
            "env": [
                {
                    "name": "DOMINO_DEV_MODE",
                    "value": platform_config['kind']["dev_mode"]
                },
            ],
            "images": {
                "useDefaultImageForMigration": False,
                "airflow": {
                    "repository": "taufferconsulting/flowui-airflow-base", # TODO change to prod # TODO change to domino image name when we have it
                    "tag": "latest",
                    "pullPolicy": "IfNotPresent"
                }
            },
            "extraSecrets": {
                "airflow-ssh-secret": {
                    "data": airflow_ssh_config_parsed
                }
            },
            "dags": {
                "gitSync": {
                    "enabled": True,
                    "wait": 60,
                    "repo": f"ssh://git@github.com/{platform_config['github']['DOMINO_GITHUB_WORKFLOWS_REPOSITORY']}.git",
                    "branch": "main",
                    "subPath": "workflows",
                    "sshKeySecret": "airflow-ssh-secret"
                }
            },
            **workers,
            **scheduler,
        }
    }

    # Add airflow helm repository
    # TODO check why is not working with remote helm chart
    # subprocess.run([
    #     "helm", "repo", "add", "apache-airflow", "https://airflow.apache.org"
    # ])
    # Write yaml to temp file and install domino airflow
    with NamedTemporaryFile(suffix='.yaml', mode="w") as fp:
        yaml.dump(airflow_values_override_config, fp)
        # Install airflow
        subprocess.run([
            "helm", "upgrade",
            "-i", "-f", str(fp.name),
            "domino-airflow",
            domino_airlflow_helm_path,
        ])

    # For each path create a pv and pvc
    if platform_config['kind']['dev_mode'] == 'local':
        config.load_kube_config()
        k8s_client = client.CoreV1Api()
        v1 = client.RbacAuthorizationV1Api()

        # Create service account role binding with admin access for airflow worker
        role_binding_name_worker = "full-access-user-clusterrolebinding-worker"
        sa_name = "domino-airflow-worker"
        cluster_role_binding_worker = client.V1ClusterRoleBinding(
            metadata=client.V1ObjectMeta(name=role_binding_name_worker),
            subjects=[
                client.V1Subject(
                    kind="ServiceAccount",
                    name=sa_name,
                    namespace="default"
                )
            ],
            role_ref=client.V1RoleRef(
                kind="ClusterRole",
                name="cluster-admin",
                api_group="rbac.authorization.k8s.io"
            )
        )
        console.print('Creating RBAC Worker Authorization for local dev')
        v1.create_cluster_role_binding(cluster_role_binding_worker)

        role_binding_name_scheduler = "full-access-user-clusterrolebinding-scheduler"
        sa_name = "domino-airflow-scheduler"
        cluster_role_binding_scheduler = client.V1ClusterRoleBinding(
            metadata=client.V1ObjectMeta(name=role_binding_name_scheduler),
            subjects=[
                client.V1Subject(
                    kind="ServiceAccount",
                    name=sa_name,
                    namespace="default"
                )
            ],
            role_ref=client.V1RoleRef(
                kind="ClusterRole",
                name="cluster-admin",
                api_group="rbac.authorization.k8s.io"
            )
        )
        console.print('Creating RBAC Scheduler Authorization for local dev')
        v1.create_cluster_role_binding(cluster_role_binding_scheduler)

        for project_name in platform_config["local_pieces_repositories"].keys():
            console.log(f"Creating PV and PVC for {project_name}...")
            # Check if pv already exists
            persistent_volume_name = 'pv-{}'.format(str(project_name.lower().replace('_', '-')))
            persistent_volume_claim_name = 'pvc-{}'.format(str(project_name.lower().replace('_', '-')))
            pvc_exists = False
            try:
                k8s_client.read_namespaced_persistent_volume_claim(name=persistent_volume_claim_name, namespace='default')
                pvc_exists = True
            except client.rest.ApiException as e:
                if e.status != 404:
                    raise e

            if not pvc_exists:
                pvc = client.V1PersistentVolumeClaim(
                    metadata=client.V1ObjectMeta(name=persistent_volume_claim_name),
                    spec=client.V1PersistentVolumeClaimSpec(
                        access_modes=["ReadOnlyMany"],
                        volume_name=persistent_volume_name,
                        resources=client.V1ResourceRequirements(
                            requests={"storage": "300Mi"}
                        ),
                        storage_class_name="standard"
                    )
                )
                k8s_client.create_namespaced_persistent_volume_claim(namespace="default", body=pvc)

            pv_exists = False
            try:
                k8s_client.read_persistent_volume(name=persistent_volume_name)
                pv_exists = True
            except client.rest.ApiException as e:
                if e.status != 404:
                    raise e

            if not pv_exists:
                pv = client.V1PersistentVolume(
                    metadata=client.V1ObjectMeta(name=persistent_volume_name),
                    spec=client.V1PersistentVolumeSpec(
                        access_modes=["ReadWriteOnce"],
                        capacity={"storage": "1Gi"},
                        persistent_volume_reclaim_policy="Retain",
                        storage_class_name="standard",
                        host_path=client.V1HostPathVolumeSource(path=f"/pieces_repositories/{project_name}"),
                        claim_ref=client.V1ObjectReference(
                            namespace="default",
                            name=persistent_volume_claim_name,
                            kind="PersistentVolumeClaim"
                        ),
                        node_affinity=client.V1VolumeNodeAffinity(
                            required=client.V1NodeSelector(
                                node_selector_terms=[
                                    client.V1NodeSelectorTerm(
                                        match_expressions=[
                                            client.V1NodeSelectorRequirement(
                                                key="kubernetes.io/hostname",
                                                operator="In",
                                                values=["domino-cluster-worker"]
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    )
                )
                k8s_client.create_persistent_volume(body=pv)
        
        if platform_config['local_domino_repository'].get('DOMINO_LOCAL_DOMINO_REPOSITORY'):
            console.print("Creating PV's and PVC's for Local Domino Package...")
            # Create pv and pvc for local dev domino
            pvc = client.V1PersistentVolumeClaim(
                metadata=client.V1ObjectMeta(name="domino-dev-volume-claim"),
                spec=client.V1PersistentVolumeClaimSpec(
                    access_modes=["ReadWriteMany"],
                    volume_name="domino-dev-volume",
                    resources=client.V1ResourceRequirements(
                        requests={"storage": "300Mi"}
                    ),
                    storage_class_name="standard"
                )
            )
            k8s_client.create_namespaced_persistent_volume_claim(namespace="default", body=pvc)
            pv = client.V1PersistentVolume(
                metadata=client.V1ObjectMeta(name="domino-dev-volume"),
                spec=client.V1PersistentVolumeSpec(
                    storage_class_name="standard",
                    access_modes=["ReadWriteMany"],
                    capacity={"storage": "2Gi"},
                    host_path=client.V1HostPathVolumeSource(path="/domino_dev"), # TODO - change this to domino_dev once we have a domino_dev in the docker images
                    claim_ref=client.V1ObjectReference(
                        namespace="default",
                        name="domino-dev-volume-claim",
                    ),
                    node_affinity=client.V1VolumeNodeAffinity(
                        required=client.V1NodeSelector(
                            node_selector_terms=[
                                client.V1NodeSelectorTerm(
                                    match_expressions=[
                                        client.V1NodeSelectorRequirement(
                                            key="kubernetes.io/hostname",
                                            operator="In",
                                            values=["domino-cluster-worker"]
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                )
            )
            k8s_client.create_persistent_volume(body=pv)

    console.print("")
    console.print("K8s resources created successfully!", style=f"bold {COLOR_PALETTE.get('success')}")

    console.print("You can now access the Domino frontend at: http://localhost/")
    console.print("and the Backend API at: http://localhost/api/")