# import pytest
# from kfp import compiler
# from kfp import dsl

# from artistml_sdk.gateway import kfp_client
# from artistml_sdk.lib import config

# kfp_host = config.test.get_val(
#     "kfp",
#     "host",
# )
# kfp_port = config.test.get_val(
#     "kfp",
#     "port",
# )

# # kfp_client.set_endpoint(endpoint=f"http://{kfp_host}:{kfp_port}", )

# @dsl.component
# def addition_component(num1: int, num2: int) -> int:
#     return num1 + num2

# @dsl.pipeline(name='addition-pipeline')
# def my_pipeline(a: int, b: int, c: int = 10):
#     add_task_1 = addition_component(num1=a, num2=b)
#     add_task_2 = addition_component(num1=add_task_1.output, num2=c)

# cmplr = compiler.Compiler()

# @pytest.mark.skip(reason="TODO: delete kubeflow")
# def test_create_experiment():
#     assert kfp_client.api_client.create_experiment(
#         name="sylvan-test-1",
#         namespace="artistml-2022",
#     ).id is not None
#     assert len(
#         kfp_client.api_client.list_experiments(
#             namespace="artistml-2022", ).experiments) > 0
