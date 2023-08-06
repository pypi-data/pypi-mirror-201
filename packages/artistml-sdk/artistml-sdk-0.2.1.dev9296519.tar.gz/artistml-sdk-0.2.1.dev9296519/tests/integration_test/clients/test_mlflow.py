import tempfile
from random import randint
from random import random

import mlflow
import pytest

from artistml_sdk.lib import config

mlflow_host = config.test.get_val(
    "mlflow",
    "host",
)
mlflow_port = config.test.get_val(
    "mlflow",
    "port",
)


@pytest.fixture(scope="module")  #一个module里的所有函数共用一个句柄实例
def start_mlflow():
    # 连接服务
    mlflow.set_tracking_uri(f"http://{mlflow_host}:{mlflow_port}")
    mlflow.set_experiment("my-experiment")
    mlflow.start_run()
    yield "连接句柄"
    #关闭句柄
    mlflow.end_run()


def test_log_metric(start_mlflow):
    # 记录参数
    mlflow.log_param("param1", randint(0, 100))
    # 记录指标
    mlflow.log_metric("foo", random())
    mlflow.log_metric("foo", random() + 1)
    mlflow.log_metric("foo", random() + 2)


def test_log_artifacts(start_mlflow):
    # 记录输出文件
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(f"{tmpdirname}/test.txt", "w") as f:
            f.write("hello world!")
    mlflow.log_artifacts(f"{tmpdirname}")
