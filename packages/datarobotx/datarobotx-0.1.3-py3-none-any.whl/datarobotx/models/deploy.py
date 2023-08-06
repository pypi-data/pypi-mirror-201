#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from abc import ABC, abstractmethod
import datetime
import io
import logging
import os
import pickle
import subprocess
import sys
import tempfile
import textwrap
from typing import Any, Callable, cast, Dict, Iterable, List, Optional, Tuple, Union

import pkg_resources  # type: ignore[import]

import datarobotx.client.deployments as deploy_client
from datarobotx.common import utils
from datarobotx.common.config import context
from datarobotx.models.deployment import Deployment
from datarobotx.models.model import Model

logger = logging.getLogger("drx")


def deploy(
    model: Any,
    *args: Any,
    target: Optional[str] = None,
    classes: Optional[List[str]] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    hooks: Optional[Dict[str, Callable]] = None,  # type: ignore[type-arg]
    extra_requirements: Optional[List[str]] = None,
    **kwargs: Any,
) -> Deployment:
    """
    Deploy a model to MLOps

    If model object is a non-DR model, will build and configure an appropriate
    supporting custom environment and custom inference model within DataRobot as
    part of deployment.

    Parameters
    ----------
    model : Any
        The model object to deploy. See the drx documentation for additional
        information on supported model types.
    *args : Any, optional
        Additional model objects; required for certain model types,
        e.g. Huggingface tokenizer + pre-trained model
    target : str, optional
        Name of the target variable; required for supervised model types
    classes : list of str, optional
        Names of the target variable classes; required for supervised classification
        problems; for binary classification, the first item should be the positive
        class
    name : str, optional
        Name of the ML Ops deployment
    description: str, optional
        Short description for the ML Ops deployment
    extra_requirements: list of str, optional
        For custom model deployments: additional python pypi package names to include
        in the custom environment. Default behavior is to include standard dependencies
        for the model type
    hooks: dict of callable, optional
        For custom model deployments: additional hooks to include with the deployment;
        see the DataRobot User Models documentation for details on supported hooks
    **kwargs
        Additional keyword arguments that may be model specific

    Returns
    -------
    deployment : Deployment
        Resulting ML Ops deployment; returned immediately and automatically updated
        asynchronously as the deployment process proceeds

    Examples
    --------

    scikit-learn pipeline


    >>> import sklearn
    >>>
    >>> pipe : sklearn.pipeline # assumes pipe has been defined & fit elsewhere
    >>> deployment_1 = deploy(pipe,
    ...                       target='my_target',
    ...                       classes=['my_pos_class', 'my_neg_class'])

    scikit-learn pipeline with custom preprocessing hook

    >>> import io
    >>> import pandas as pd
    >>>
    >>> df : pd.DataFrame # assumes training data was previously read elsewhere
    >>> my_types = df.dtypes
    >>> def force_schema(input_binary_data, *args, **kwargs):
    ...     buffer = io.BytesIO(input_binary_data)
    ...     return pd.read_csv(buffer, dtype=dict(my_types))
    >>>
    >>> deployment_2 = deploy(pipe,
    ...                       target='my_target',
    ...                       classes=['my_pos_class', 'my_neg_class'],
    ...                       hooks={'read_input_data': force_schema})

    """

    if isinstance(model, Model):
        return model.deploy()
    else:
        deployment = Deployment()
        deployer = CustomDeployer(
            deployment,
            model,
            *args,
            target=target,
            classes=classes,
            name=name,
            description=description,
            hooks=hooks,
            extra_requirements=extra_requirements,
            **kwargs,
        )
        utils.create_task_new_thread(deployer.deploy())
        return deployment


class CustomDeployer(ABC):
    def __init__(
        self,
        destination: Deployment,
        model: Any,
        *args: Any,
        target: Optional[str] = None,
        classes: Optional[List[str]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        hooks: Optional[Dict[str, Callable]] = None,  # type: ignore[type-arg]
        extra_requirements: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        # Reference to resulting deployment object
        self.destination = destination

        self.model = model
        self.extra_models = args

        # Environment config
        self.dockerfile = _DOCKERFILE_TEMPLATE
        self.requirements_txt = ""
        self.dr_requirements_txt = _DRUM_REQ
        self.extra_requirements = extra_requirements
        self.start_server_sh = _START_SERVER_SH_TEMPLATE

        # Custom inference model spec config
        self.name = name or utils.generate_name()
        self.description = description or "Auto-deployed by drx on {:%Y-%m-%d %H:%M:%S}".format(
            datetime.datetime.now()
        )
        self.model_spec_json: Dict[str, Any] = {}

        # Custom.py hooks e.g. score()
        self.hooks = hooks
        self.custom_py = ""
        if hooks is not None:
            self.dr_requirements_txt += _CLOUDPICKLE_REQ

        # Payloads
        self.env_spec_json: Dict[str, Any] = {}
        self.env_payload: Tuple[str, Union[bytes, io.BytesIO]] = None  # type: ignore[assignment]
        self.model_payload: List[Tuple[str, Any]] = []

        self.model_exporter = ModelExporter(model, *args, target=target, classes=classes, **kwargs)

    async def deploy(self) -> None:
        logger.info("Deploying custom model", extra={"is_header": True})
        logger.info("Preparing model and environment...")

        self.prepare_env()
        self.prepare_json_config()
        self.prepare_custom_hooks()
        await self.prepare_payloads()

        self.destination._deployment_id = await self.transmit()
        logger.info("Custom model deployment complete", extra={"is_header": True})

    def prepare_env(self) -> None:
        """Prepares the custom environment needed to score with the provided model."""
        self.build_requirements()
        self.update_dockerfile()

    def build_requirements(self) -> None:
        """Capture and pin versions of dependencies."""
        env = {}
        for ws in pkg_resources.working_set:
            name, version = str(ws).split()
            env[name] = version
        model_requirements = self.model_exporter.get_requirements()
        for pkg in model_requirements:
            if pkg in env:
                self.requirements_txt += pkg + "==" + env[pkg] + "\n"
        if self.extra_requirements is not None:
            for pkg in self.extra_requirements:
                if pkg in env and pkg not in model_requirements:
                    self.requirements_txt += pkg + "==" + env[pkg] + "\n"

    def update_dockerfile(self) -> None:
        """
        Updates the custom dockerfile for running the provided model to reflect
        installing the approrpiate python version using pyenv.
        """
        version_str = self.get_python_version()
        self.dockerfile = self.dockerfile.format(version_str=version_str)

    def prepare_custom_hooks(self) -> None:
        """
        Generate a custom.py file for DRUM
        """
        if self.hooks is None:
            return
        if not set(self.hooks).issubset(_HOOK_TEMPLATES):
            valid_hooks_str = ", ".join(_HOOK_TEMPLATES.keys())
            raise ValueError(f"deploy() supports the following hooks: {valid_hooks_str}")

        impl_hooks = ", ".join(f"'{hook}'" for hook in self.hooks.keys())
        self.custom_py += _HOOK_TEMPLATES["init"].format(
            timestamp=datetime.datetime.now(), impl_hooks=impl_hooks
        )
        for hook in self.hooks:
            if hook != "init":
                self.custom_py += _HOOK_TEMPLATES[hook]

    @staticmethod
    def get_python_version() -> str:
        """Return running python interpreter version as a string e.g. '3.7'."""
        version = sys.version_info
        major = version.major
        minor = version.minor
        micro = version.micro
        if major != 3 or minor > 9 or minor < 4:
            raise TypeError("deploy() supports python >=3.4, <3.10")
        return f"{major}.{minor}.{micro}"

    async def prepare_payloads(self) -> None:
        """
        Build a zip archive for a custom environment to be uploaded
        to DataRobot and also export the model itself.

        Updates dpeloyer payload attributes ready for REST API:
        env_payload, model_payload
        where
        env_payload = (env_filename, env_archive_data)
        model_payload = [(model_file1_name, file1_data),
                         (model_file2_name, file2_data), ...]
        """
        env_contents = [
            ("Dockerfile", self.dockerfile.encode()),
            ("requirements.txt", self.requirements_txt.encode()),
            ("dr_requirements.txt", self.dr_requirements_txt.encode()),
            ("start_server.sh", self.start_server_sh.encode()),
            ("__init__.py", "".encode()),
        ]
        env_filename = "drx_autogenerated_env_{:%Y-%m-%d_%Hh%Mm%Ss}.zip".format(
            datetime.datetime.now()
        )
        env_data = utils.archive(env_contents)

        raw_model_payload = await self.model_exporter.export_model(self.name)
        hooks_payload = await self.export_hooks()

        self.env_payload = (env_filename, env_data)
        self.model_payload = raw_model_payload + hooks_payload

    def prepare_json_config(self) -> None:
        """
        Prepare the json config parameters the DataRobot
        custom inference env and model endpoints expect.
        """
        base_model_json = {
            "name": self.name,
            "description": self.description,
            "language": "Python " + self.get_python_version(),
            "targetName": self.model_exporter.target,
            "customModelType": "inference",
        }
        model_config = self.model_exporter.get_dr_config()

        self.model_spec_json = {**base_model_json, **model_config}  # merge
        self.env_spec_json = {
            "name": "[Custom] " + self.name,
            "description": self.description,
        }

    async def export_hooks(self) -> List[Tuple[str, bytes]]:
        """Export any user-provided custom hooks for the model
        as a custom.py file and associated cloudpickles.

        Returns a list of tuples for each file [(filename, data), ...]
        """
        if self.hooks is None:
            return []

        import cloudpickle

        hooks_payload = [("custom.py", self.custom_py.encode())]
        for hook in self.hooks:
            hooks_payload.append((hook + ".pickle", cloudpickle.dumps(self.hooks[hook])))
        return hooks_payload

    async def transmit(self) -> str:
        """Transmit the custom model and environment to DataRobot and deploy."""
        env_id = cast(str, await deploy_client.create_custom_env(self.env_spec_json))
        env_version_id = cast(
            str, await deploy_client.create_custom_env_version(env_id, self.env_payload)
        )
        self._log_created_environment(
            environment_id=env_id,
            environment_name=self.env_spec_json["name"],
            python_version=self.get_python_version(),
            requirements=self.requirements_txt,
            dr_requirements=self.dr_requirements_txt,
        )
        logger.info("Awaiting custom environment build...")
        await deploy_client.await_env_build(env_id, env_version_id)

        logger.info("Configuring and uploading custom model...")
        model_id = cast(str, await deploy_client.create_custom_model(self.model_spec_json))
        model_version_id = cast(
            str,
            await deploy_client.create_custom_model_version(env_id, model_id, self.model_payload),
        )
        self._log_registered_custom_model(
            model_id=model_id,
            model_name=self.model_spec_json["name"],
            target_type=self.model_spec_json["targetType"],
        )

        logger.info("Creating and deploying model package...")
        package_id = await deploy_client.create_custom_model_package(
            model_id, model_version_id, env_id, env_version_id
        )
        deploy_id = await deploy_client.deploy_from_package(package_id, model_id)  # type: ignore[arg-type]
        self._log_created_deployment(
            deployment_id=deploy_id, deployment_name=self.model_spec_json["name"]
        )
        return deploy_id

    @staticmethod
    def _log_created_environment(
        environment_id: str,
        environment_name: str,
        python_version: str,
        requirements: str,
        dr_requirements: str,
    ) -> None:
        url = context._webui_base_url + f"/model-registry/custom-environments/{environment_id}"
        requirements_str = textwrap.indent(
            "python " + python_version + "\n" + dr_requirements + requirements, "  "
        )
        msg = (
            f"Configured environment [{environment_name}]({url}) "
            + "with requirements:\n"
            + f"{requirements_str}"
        )
        logger.info(msg)

    @staticmethod
    def _log_registered_custom_model(model_id: str, model_name: str, target_type: str) -> None:
        url = context._webui_base_url + f"/model-registry/custom-models/{model_id}/info"
        msg = f"Registered custom model [{model_name}]({url}) " + f"with target type: {target_type}"
        logger.info(msg)

    @staticmethod
    def _log_created_deployment(deployment_id: str, deployment_name: str) -> None:
        url = context._webui_base_url + f"/deployments/{deployment_id}/overview"
        msg = f"Created deployment [{deployment_name}]({url})"
        logger.info(msg)


class ModelExporter:
    """Implements export (serialization) and requirement determination for arbitrary
    models."""

    def __init__(
        self,
        *models: Iterable[Any],
        target: Optional[str] = None,
        classes: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.target = target
        self.classes = classes
        self.exporter: Union[SklearnExporter, TransformersOnnxExporter] = None  # type: ignore[assignment]
        import sklearn
        from transformers import PreTrainedModel, PreTrainedTokenizerBase, TFPreTrainedModel

        model = models[0]
        if isinstance(model, sklearn.base.BaseEstimator):
            self.exporter = SklearnExporter(model)
        elif isinstance(model, (TFPreTrainedModel, PreTrainedModel, PreTrainedTokenizerBase)):
            if "feature" not in kwargs:
                raise TypeError("Huggingface ONNX support requires the keyword argument 'feature'")
            self.exporter = TransformersOnnxExporter(*models, feature=kwargs["feature"])
        else:
            model_type_str = type(model).__name__
            raise TypeError(f"deploy() does not support models of type {model_type_str}")

    def get_dr_config(self) -> Dict[str, Union[int, str]]:
        """Compute model-specific json config DataRobot expects for this combination
        of model objs + target + classes.

        Returns dict of model-specific config."""
        model_config = self.exporter.dr_model_spec
        if "targetType" not in model_config:
            model_config["targetType"] = self.infer_dr_target_type()
        if self.classes:  # classification problem
            if len(self.classes) > 2:
                model_config["classLabels"] = self.classes
            else:
                model_config["positiveClassLabel"] = self.classes[0]
                model_config["negativeClassLabel"] = self.classes[1]
        return model_config

    def infer_dr_target_type(self) -> str:
        """Infer the DataRobot MLOps deployment target type.

        Returns dr.TARGET_TYPE enum value
        """
        if self.classes:  # classification problem
            if len(self.classes) > 2:
                return "Multiclass"
            else:
                return "Binary"
        elif self.target:  # regression
            return "Regression"
        else:  # anomaly
            return "Anomaly"

    def get_requirements(self) -> List[str]:
        """Return requirements for this model in pip requirements.txt format
        as a str object."""
        return self.exporter.requirements

    async def export_model(self, model_name: str) -> List[Tuple[str, Union[bytes, io.BytesIO]]]:
        """Serialize the model(s) to bytes object(s) that
        can later be uploaded over HTTP.

        Returns a list of tuples [(file_name, data), ...]"""
        return await self.exporter.export_model(model_name)


class BaseExporter(ABC):
    """Abstract base class for a model exporter."""

    def __init__(self, model: Model, *extra_models: List[Model]):
        self.model = model
        self.extra_models = extra_models

    @property
    def dr_model_spec(self) -> Dict[str, Any]:
        """Returns dictionary of any additional model-specific DataRobot config
        that will be passed to DR upon custom model creation."""
        return {}

    @abstractmethod
    async def export_model(self, model_name: str) -> List[Tuple[str, Union[bytes, io.BytesIO]]]:
        """Serialize the model and prepare for upload over HTTP

        Returns [(file_name1, data1), (file_name2, data2), ...]
        file_name is a string
        data1 is of type io.BytesIO or bytes
        """

    @property
    @abstractmethod
    def requirements(self) -> List[str]:
        pass


class SklearnExporter(BaseExporter):
    # latest deps according to pip as of 6/10/2022
    requirements = [
        "scikit-learn",
        "joblib",
        "numpy",
        "scipy",
        "threadpoolctl",
    ]

    async def export_model(self, model_name: str) -> List[Tuple[str, Union[bytes, io.BytesIO]]]:
        file_name = f"{model_name}.pkl"
        data = pickle.dumps(self.model)
        return [(file_name, data)]


class TransformersOnnxExporter(BaseExporter):
    requirements = [
        "transformers",
        "onnxruntime",
    ]
    dr_model_spec = {"maximumMemory": 4096 * 1024 * 1024, "targetType": "Unstructured"}

    def __init__(self, *args: Any, feature: Optional[str] = "default", **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.tokenizer = None
        self.feature = feature

        from transformers import (
            FeatureExtractionMixin,
            PreTrainedModel,
            PreTrainedTokenizerBase,
            TFPreTrainedModel,
        )

        models = (self.model,) + self.extra_models
        for model in models:
            if isinstance(model, PreTrainedTokenizerBase):
                self.tokenizer = model
            elif isinstance(model, (TFPreTrainedModel, PreTrainedModel)):
                self.model = model
            elif isinstance(model, FeatureExtractionMixin):
                raise NotImplementedError(
                    "Support for FeatuereExtractionMixin not implemented yet!"
                )

    async def export_model(self, model_name: str) -> List[Tuple[str, Union[bytes, io.BytesIO]]]:
        py_executable = sys.executable
        with tempfile.TemporaryDirectory() as path:
            self.tokenizer.save_pretrained(path)  # type: ignore[union-attr]
            self.model.save_pretrained(path)  # type: ignore[attr-defined]
            command = [
                f"{py_executable}",
                "-m",
                "transformers.onnx",
                "--model",
                f"{path}",
                "--feature",
                f"{self.feature}",
                f"{path}",
            ]
            logger.info("Performing transformers.onnx export...")
            subprocess.run(command, stderr=subprocess.STDOUT, check=True)
            with open(f"{path}/model.onnx", "rb") as f:
                model_data = io.BytesIO(f.read())
                model_file_name = "model.onnx"
        model_payload = [(model_file_name, model_data)]

        tokenizer_payload = []
        with tempfile.TemporaryDirectory() as path:
            self.tokenizer.save_pretrained(path)  # type: ignore[union-attr]
            for file in os.listdir(path):
                if not file.startswith("."):
                    with open(path + "/" + file, "rb") as f:
                        data = io.BytesIO(f.read())
                        tokenizer_payload.append((file, data))

        return model_payload + tokenizer_payload  # type: ignore[return-value]


_HOOK_TEMPLATES = {
    "init": """# custom.py autogenerated by datarobotx {timestamp:%Y-%m-%d %H:%M:%S}

_HOOK_IMPLS = {{}}

def init(code_dir, **kwargs):
    import pickle

    hooks = [{impl_hooks}]
    for hook in hooks:
        with open(code_dir + '/' + hook + '.pickle', 'rb') as f:
            _HOOK_IMPLS[hook] = pickle.load(f)

    if 'init' in hooks:
        _HOOK_IMPLS['init'](code_dir, **kwargs)
""",
    "read_input_data": """
def read_input_data(input_binary_data):
    return _HOOK_IMPLS['read_input_data'](input_binary_data)
""",
    "load_model": """
def load_model(code_dir):
    return _HOOK_IMPLS['load_model'](code_dir)
""",
    "transform": """
def transform(data, model):
    return _HOOK_IMPLS['transform'](data, model)
""",
    "score": """
def score(data, model, **kwargs):
    return _HOOK_IMPLS['score'](data, model, **kwargs)
""",
    "score_unstructured": """
def score_unstructured(model, data, **kwargs):
    return _HOOK_IMPLS['score_unstructured'](model, data, **kwargs)
""",
    "post_process": """
def post_process(predictions, model):
    return _HOOK_IMPLS['post_process'](predictions, model)
""",
}

_DRUM_REQ = "datarobot-drum>=1.9.3\n"
_CLOUDPICKLE_REQ = "cloudpickle>=2.0.0\n"

_START_SERVER_SH_TEMPLATE = """#!/bin/sh
echo "Starting Custom Model environment with DRUM prediction server"
echo "Environment variables:"
env
echo

CMD="drum server $@"
echo "Executing command: ${CMD}"
echo
exec ${CMD}
"""

# Inspired by git repo: datarobot-user-models/public_dropin_environments
_DOCKERFILE_TEMPLATE = """
# This is the default base image for use with user models and workflows.
# It contains a variety of common useful data-science packages and tools.
FROM datarobot/dropin-env-base:latest

# Install pyenv and the desired version of python

WORKDIR /opt/
RUN apt-get update
RUN apt-get install -y git curl wget make build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev

RUN git clone --depth=1 https://github.com/pyenv/pyenv.git pyenv

ENV PYENV_ROOT="/opt/pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN pyenv install {version_str}
RUN pyenv global {version_str}
RUN pip3 install --upgrade pip

COPY dr_requirements.txt dr_requirements.txt
RUN pip3 install -r dr_requirements.txt  && \
    rm -rf dr_requirements.txt

# Install the list of custom Python requirements, e.g. keras, xgboost, etc.
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir && \
    rm -rf requirements.txt

RUN chmod -R 755 $PYENV_ROOT/versions
RUN chmod -R 755 $PYENV_ROOT/shims

# Copy the drop-in environment code into the correct directory
# Code from the custom model tarball can overwrite the code here
ENV HOME=/opt CODE_DIR=/opt/code ADDRESS=0.0.0.0:8080
WORKDIR ${{CODE_DIR}}
COPY ./ ${{CODE_DIR}}

ENV WITH_ERROR_SERVER=1
# Uncomment the following line to switch from Flask to uwsgi server
#ENV PRODUCTION=1 MAX_WORKERS=1 SHOW_STACKTRACE=1

ENTRYPOINT ["/opt/code/start_server.sh"]"""
