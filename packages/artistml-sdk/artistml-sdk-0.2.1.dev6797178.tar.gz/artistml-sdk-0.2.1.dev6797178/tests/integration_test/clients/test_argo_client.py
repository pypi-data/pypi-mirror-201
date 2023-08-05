import os

import yaml
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest, )

from artistml_sdk.clients import ArgoClient
from artistml_sdk.gateway import argo_client
from artistml_sdk.lib import config

argo_host = config.test.get_val(
    "argo",
    "host",
)
argo_port = config.test.get_val(
    "argo",
    "port",
)

argo_client.set_endpoint(endpoint=f"{argo_host}:{argo_port}")
client = ArgoClient()


def test_create_workflow():
    yaml_path = os.path.join(os.path.dirname(__file__), "workflow.yaml")
    with open(yaml_path, "r") as f:
        manifest = yaml.safe_load(f.read())

    api_response = client.create_workflow(
        namespace="undefined",
        body=IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(
            workflow=manifest, _check_type=False),
    )
    assert api_response.metadata["name"].startswith("hello-world")
