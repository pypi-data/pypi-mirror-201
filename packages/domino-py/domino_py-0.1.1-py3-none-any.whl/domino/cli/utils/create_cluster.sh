#!/bin/bash

cluster_name=$1

# Delete any existing clusters with provided name
kind delete cluster --name cluster_name
sleep 2

# Create a kind cluster
kind create cluster --name flowui-cluster --config kind-cluster-config.yaml

# kind load docker-image taufferconsulting/flowui-airflow-base:0.0.1 --name flowui-cluster --nodes flowui-cluster-worker

# helm dependency build dependency

# helm upgrade -i -f airflow_helm_chart/values-dev.yaml airflow airflow_helm_chart/
# helm upgrade --set github_access_token=$GITHUB_ACCESS_TOKEN -i -f flowui_helm_chart/values-dev.yaml flowui flowui_helm_chart/