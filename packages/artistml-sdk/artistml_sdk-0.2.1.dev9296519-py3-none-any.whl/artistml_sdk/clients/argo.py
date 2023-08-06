from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow import IoArgoprojWorkflowV1alpha1Workflow
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest, )
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_template import (
    IoArgoprojWorkflowV1alpha1WorkflowTemplate, )
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_template_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowTemplateCreateRequest, )

from ..gateway import argo_client
from ..gateway import try_request_grpc


class ArgoClient:

    @staticmethod
    def tag():
        return "hello!"

    @property
    def _stub(self):
        """
        The function returns the vela client object
        :return: The vela client object
        """
        return argo_client

    @try_request_grpc
    def create_workflow(
        self,
        namespace: str,
        body: IoArgoprojWorkflowV1alpha1WorkflowCreateRequest,
    ) -> IoArgoprojWorkflowV1alpha1Workflow:
        return self._stub.workflow.create_workflow(
            namespace=namespace,
            body=body,
            _check_return_type=False,
        )

    @try_request_grpc
    def get_workflow(
        self,
        namespace,
        name,
        **kwargs,
    ):
        return self._stub.workflow.get_workflow(
            namespace,
            name,
            **kwargs,
        )

    @try_request_grpc
    def create_workflow_template(
        self,
        namespace: str,
        body: IoArgoprojWorkflowV1alpha1WorkflowTemplateCreateRequest,
    ) -> IoArgoprojWorkflowV1alpha1WorkflowTemplate:
        if body.template.metadata.name:
            self.delete_workflow_template(namespace,
                                          body.template.metadata.name)
        return self._stub.workflow_template.create_workflow_template(
            namespace,
            body,
            _check_return_type=False,
        )

    @try_request_grpc
    def delete_workflow_template(
        self,
        namespace: str,
        name: str,
        **kwargs,
    ):
        return self._stub.workflow_template.delete_workflow_template(
            namespace, name, **kwargs)
