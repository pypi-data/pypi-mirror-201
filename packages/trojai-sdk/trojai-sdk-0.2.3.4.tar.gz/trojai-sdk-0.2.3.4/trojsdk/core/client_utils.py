import json
import numpy as np
from typing import Tuple
from pathlib import Path

from trojsdk.client import TrojClient
from trojsdk.config.base import BaseTrojConfig
from trojsdk.config.nlp import NLPTrojConfig
from trojsdk.config.tabular import TabularTrojConfig
from trojsdk.config.vision import VisionTrojConfig
from trojsdk.core import data_utils, troj_logging

log = troj_logging.getLogger(__file__)

"""
The troj job handler class wraps the client and stores all details relevant to a given job or session.
"""


def submit_evaluation(
    path_to_config: str = None, config: dict = None, docker_metadata=None, k8s_metadata=None, nossl=False
) -> "TrojJobHandler":
    """
    Submit a job using the specified config.
    Either path_to_config or config are required, path_to_config takes priority.

    :param path_to_config: The path of a JSON file containing your config for the evaluation.
    :param config: A dict containing your config for the evaluation.
    :param docker_metadata: A dict containing two entries; "docker-image" and "docker_secret_name". Default values are trojai/troj-engine-base-<type>:<tabluar>-predev-latest and trojaicreds respectively.
    """

    if path_to_config is not None:
        config = data_utils.load_json_from_disk(Path(path_to_config))
        log.info("JSON loaded from disk.")

    config, docker_metadata, k8s_metadata = config_from_dict(config, docker_metadata)
    tjh = TrojJobHandler()
    response = tjh.post_job_to_endpoint(config, docker_metadata, k8s_metadata, nossl)
    log.info("Config posted to endpoint")
    log.info("Response: " + str(response))

    return tjh


def config_from_dict(
    config: dict, docker_metadata: dict = None, k8s_metadata: dict = None
) -> Tuple[BaseTrojConfig, dict]:
    """
    :param config: The config file to be converted to a BaseTrojConfig type; NLPTrojConfig, TabularTrojConfig, or VisionTrojConfig. Determined by "task_type" within the config.
    :type config: dict
    :param docker_metadata: The dict containing the current docker data, if any. If supplied, this field will be prioritized over the docker_metadata in the config. Defaults to None.
    :type docker_metadata: dict, optional

    :return: The BaseTrojConfig type object, with "docker_metadata" popped off, if it existed. Tuples with docker_metadata with the following descending priority: parameter from this func, field from config, default value for given task_type.
    :rtype: Tuple[BaseTrojConfig, dict]
    """

    config_km = None
    if config.get("k8s_metadata"):
        config_km = config.pop("k8s_metadata")

    if not k8s_metadata:
        if config_km:
            k8s_metadata = config_km

    config_dm = None
    if config.get("docker_metadata"):
        config_dm = config.pop("docker_metadata")

    if not docker_metadata:
        if config_dm:
            docker_metadata = config_dm
        else:
            docker_metadata = get_default_docker_metadata(config.get("task_type"))

    if not docker_metadata.get("image_pull_policy"):
        docker_metadata["image_pull_policy"] = "Always"
    if docker_metadata.get("docker_secret_name") is None:
        docker_metadata["docker_secret_name"] = "None"

    if config["task_type"] == "nlp":
        config = NLPTrojConfig.config_from_dict(config)
    elif config["task_type"] == "tabular":
        config = TabularTrojConfig.config_from_dict(config)
    elif config["task_type"] == "vision":
        config = VisionTrojConfig.config_from_dict(config)
    else:
        raise Exception(
            f"Model type {config['task_type']} not found. Please select one of [tabular, nlp, vision]."
        )

    return config, docker_metadata, k8s_metadata


def get_default_docker_metadata(task_type: str):
    docker_metadata = {
        "docker_secret_name": "trojaicreds",
        "image_pull_policy": "Always",
    }
    try:
        docker_choices_dict = {
            "tabular": "trojai/troj-engine-base-tabular:tabluar-dev-latest",
            "nlp": "trojai/troj-engine-base-nlp:nlp-dev-latest",
            "vision": "trojai/troj-engine-base-cv:cv-dev-latest",
        }
        docker_metadata["docker_image_url"] = docker_choices_dict[
            str(task_type).lower()
        ]
    except Exception as e:
        raise Exception(
            f"Model type {task_type} not found. Please select one of "
            + str(list(docker_choices_dict))
        ) from e

    return docker_metadata


class TrojJobHandler:
    def __init__(self) -> None:
        self.client = None
        self.post_response = None
        self.status_response = None

    def post_job_to_endpoint(
        self, config: BaseTrojConfig, docker_metadata: dict = None, k8s_metadata: dict = None, nossl=False
    ) -> dict:
        """
        This function posts any given config to the endpoint.

        :param config: The main configuration for the project.
        :type config: BaseTrojConfig
        :param docker_metadata: A dictionary with the following two values;
            "docker_image_url": A Docker Hub image id for any engine type.
                Ex. value: "trojai/troj-engine-base-tabular:tabluar-shawn-latest"
            "docker_secret_name": The name of the environment secret containing the credentials for Docker Hub access. This is defined in the TrojAI helm repo in the _setup.sh_ script.
        :type docker_metadata: dict, optional

        :return: Contains job_name under key "data", under key "job_name". (Dict within dict)
        :rtype: dict
        """

        self.client = TrojClient(auth_config=config.auth_config, nossl=nossl)
        res = self.client.post_job(config, docker_metadata, k8s_metadata, nossl)
        self.post_response = res
        return res

    def check_job_status(self, response: dict = None):
        """
        Check the status of a job.

        :param response: The response object received after submitting a job, defaults to None
        :type response: dict, optional
        """
        try:
            if response is None:
                response = self.post_response
                job_name = response.get("data").get("job_name")
        except Exception as e:
            raise e

        if self.client is None:
            print(
                "No jobs have been submitted yet! Call the post_job_to_endpoint and pass the required config first."
            )
        else:
            res = self.client.get_job_status(job_name)
            self.status_response = res
            return res

    def stream_job_logs(self, job_id):
        """
        This function will stream all the prints/logs from the evaluation pod as its running.
        """
        raise NotImplementedError


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)
