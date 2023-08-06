import os

import yaml
from argo_workflows.model.io_argoproj_workflow_v1alpha1_template import IoArgoprojWorkflowV1alpha1Template
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_template import (
    IoArgoprojWorkflowV1alpha1WorkflowTemplate, )
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_template_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowTemplateCreateRequest, )

from artistml_sdk.clients import ArgoClient
from artistml_sdk.gateway import argo_client
from artistml_sdk.lib import config
from artistml_sdk.lib import dict_to_argo_model

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

skill_module_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))))),
    "artistml-skill",
)


def test_create_workflow_template_for_skills():
    template_path = os.path.join(skill_module_path, "skills")
    for file_name in os.listdir(template_path):
        with open(os.path.join(template_path, file_name), "r") as f:
            temp = yaml.safe_load(f.read())

        workflow_template = dict_to_argo_model(
            IoArgoprojWorkflowV1alpha1WorkflowTemplate,
            temp,
        )
        main_template_name = workflow_template.spec.entrypoint
        main_template = [
            t for t in workflow_template.spec.templates
            if t.name == main_template_name
        ]
        assert len(
            main_template
        ) == 1, "require extractly one template match entrypoint's name"
        main_template = main_template[0]
        templates = [main_template]
        for steps in main_template.steps:
            for step in steps.value:
                node_yaml_path = os.path.join(
                    skill_module_path,
                    f"{step.name}",
                    "node.yaml",
                )
                with open(node_yaml_path, "r") as f:
                    data = yaml.safe_load(f.read())
                template = dict_to_argo_model(
                    IoArgoprojWorkflowV1alpha1Template,
                    data,
                )
                templates.append(template)
        workflow_template.spec.templates = templates

        assert client.create_workflow_template(
            "default",
            IoArgoprojWorkflowV1alpha1WorkflowTemplateCreateRequest(
                template=workflow_template),
        ).metadata['name'] == main_template.name
