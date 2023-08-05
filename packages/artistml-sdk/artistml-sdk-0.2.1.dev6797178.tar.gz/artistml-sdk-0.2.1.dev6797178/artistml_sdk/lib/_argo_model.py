import re
from typing import Dict
from typing import List

from argo_workflows.model.io_argoproj_workflow_v1alpha1_arguments import IoArgoprojWorkflowV1alpha1Arguments
from argo_workflows.model.io_argoproj_workflow_v1alpha1_parameter import IoArgoprojWorkflowV1alpha1Parameter
from argo_workflows.model.io_argoproj_workflow_v1alpha1_template import IoArgoprojWorkflowV1alpha1Template
from argo_workflows.model_utils import change_keys_js_to_python
from argo_workflows.model_utils import deserialize_model

_GOLBAL_PARAMETER_PATTERN = re.compile(r"workflow.parameters.([\w\d_]+)")


def dict_to_argo_model(clazz, data):
    """
    convert dict to argo_workflows model
    """
    if isinstance(data, List):
        if isinstance(clazz, List):
            _clazz = clazz[0]
            for i, value in enumerate(data):
                data[i] = dict_to_argo_model(_clazz, value)
            return data
        elif hasattr(clazz, "openapi_types"):
            _clazz = clazz.openapi_types["value"][0][0]
            for i, value in enumerate(data):
                data[i] = dict_to_argo_model(_clazz, value)
            return deserialize_model(
                model_data=data,
                model_class=clazz,
                path_to_item=(),
                check_type=True,
                configuration=None,
                spec_property_naming=False,
            )
        return data
    if isinstance(data, Dict) and hasattr(clazz, "openapi_types"):
        data = change_keys_js_to_python(data, clazz)
        for key, value in data.items():
            _clazz = clazz.openapi_types[key][0]
            data[key] = dict_to_argo_model(_clazz, value)
        return deserialize_model(
            model_data=data,
            model_class=clazz,
            path_to_item=(),
            check_type=True,
            configuration=None,
            spec_property_naming=False,
        )

    return data


def create_parameters(
    template: IoArgoprojWorkflowV1alpha1Template
) -> IoArgoprojWorkflowV1alpha1Arguments:
    # s = json.dumps(model_to_dict(template))
    parameters: List[IoArgoprojWorkflowV1alpha1Parameter] = []
    for item in _GOLBAL_PARAMETER_PATTERN.findall(template.to_str()):
        parameters.append(IoArgoprojWorkflowV1alpha1Parameter(name=item, ), )
    return IoArgoprojWorkflowV1alpha1Arguments(parameters=parameters, )
