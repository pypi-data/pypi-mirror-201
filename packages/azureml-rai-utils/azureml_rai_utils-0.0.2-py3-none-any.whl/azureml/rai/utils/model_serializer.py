# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging

from typing import Any

import os
import subprocess
import sys
import mlflow

from azureml.rai.utils.constants import (
    AUTOML_MLIMAGES_MLFLOW_MODEL_IDENTIFIER, 
    ModelTypes
)

_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def log_info(message):
    _logger.info(message)
    print(message)


class ModelSerializer:
    def __init__(self,
                 model_id: str,
                 model_type: str = "pyfunc",
                 use_model_dependency: bool = False,
                 use_conda: bool = True,
                 tracking_uri: str = None):
        self._model_id = model_id
        self._model_type = model_type
        self._use_model_dependency = use_model_dependency
        self._use_conda = use_conda
        self._tracking_uri = tracking_uri

    def save(self, model, path):
        # Nothing to do, since model is saved in AzureML
        pass

    def load(self, path):
        return self.load_mlflow_model(self._model_id)

    def load_mlflow_model(self, model_id: str) -> Any:
        tracking_uri = mlflow.get_tracking_uri()
        if not tracking_uri.startswith("azureml"):
            log_info("Current non azureml tracking uri: " + tracking_uri)
            log_info("Setting mlflow tracking uri to: " + self._tracking_uri)
            mlflow.set_tracking_uri(self._tracking_uri)
        client = mlflow.tracking.MlflowClient()

        split_model_id = model_id.rsplit(":", 1)
        model_name = split_model_id[0]
        if model_name == model_id:
            model = client.get_registered_model(model_id)
            model_uri_name = model.name
            model_uri_version = model.latest_versions[0].version
        else:
            version = split_model_id[1]
            model = client.get_model_version(model_name, version=version)
            model_uri_name = model.name
            model_uri_version = model.version

        model_uri = "models:/{}/{}".format(model_uri_name, model_uri_version)
        if self._use_model_dependency:
            try:
                if self._use_conda:
                    conda_file = mlflow.pyfunc.get_model_dependencies(
                        model_uri, format='conda')
                    log_info("MLFlow model conda file location: {}".format(
                        conda_file))
                    # call conda env update in subprocess
                    subprocess.check_call([sys.executable, "-m", "conda",
                                        "env", "update", "-f", conda_file])
                else:
                    pip_file = mlflow.pyfunc.get_model_dependencies(model_uri)
                    log_info("MLFlow model pip file location: {}".format(
                        pip_file))
                    # call pip install in subprocess
                    subprocess.check_call([sys.executable, "-m", "pip",
                                        "install", "-r", pip_file])
                log_info("Successfully installed model dependencies")
            except Exception as e:
                log_info("Failed to install model dependencies")
                log_info(e)
        else:
            log_info("Skip installing model dependencies")
        if self._model_type == ModelTypes.FASTAI:
            fastai_model = mlflow.fastai.load_model(model_uri)
            log_info("fastai_model: {0}".format(type(fastai_model)))
            log_info(f"dir(fastai_model): {dir(fastai_model)}")
            return fastai_model
        elif self._model_type == ModelTypes.PYTORCH:
            pytorch_model = mlflow.pytorch.load_model(model_uri)
            log_info("pytorch_model: {0}".format(type(pytorch_model)))
            log_info(f"dir(pytorch_model): {dir(pytorch_model)}")
            return pytorch_model
        else:
            mlflow_loaded = mlflow.pyfunc.load_model(model_uri)
            log_info("mlflow_loaded: {0}".format(type(mlflow_loaded)))
            log_info(f"dir(mlflow_loaded): {dir(mlflow_loaded)}")
            if str(type(mlflow_loaded._model_impl.python_model)).endswith(
                AUTOML_MLIMAGES_MLFLOW_MODEL_IDENTIFIER
            ):
                return mlflow_loaded
            model_impl = mlflow_loaded._model_impl
            log_info("model_impl: {0}".format(type(model_impl)))
            log_info(f"dir(model_impl): {dir(model_impl)}")
            internal_model = model_impl.python_model
            log_info(f"internal_model: {type(internal_model)}")
            log_info(f"dir(internal_model): {dir(internal_model)}")
            extracted_model = internal_model._model
            log_info(f"extracted_model: {type(extracted_model)}")
            log_info(f"dir(extracted_model): {dir(extracted_model)}")
            return extracted_model
