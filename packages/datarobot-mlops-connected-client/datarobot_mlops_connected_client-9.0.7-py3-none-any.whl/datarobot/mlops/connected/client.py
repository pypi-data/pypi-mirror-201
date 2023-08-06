#  Copyright (c) 2019 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.
#  The copyright notice above does not evidence any actual or intended publication of
#  such source code.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.

import cgi
import datetime
import logging
import math
import os
import tempfile
import time
import warnings
from contextlib import suppress

import aiohttp
import requests
from datarobot.mlops.common.aggregation_util import convert_aggregated_stats_features_to_dr_format
from datarobot.mlops.common.aggregation_util import (
    convert_aggregated_stats_predictions_to_dr_format,
)
from datarobot.mlops.common.aggregation_util import (
    convert_aggregated_stats_segment_attr_to_dr_format,
)
from datarobot.mlops.common.config import ConfigConstants
from datarobot.mlops.common.config import get_config_default
from datarobot.mlops.common.enums import DataFormat
from datarobot.mlops.common.exception import DRNotFoundException
from datarobot.mlops.common.exception import DRUnsupportedType
from datarobot.mlops.common.prediction_util import get_predictions
from datarobot.mlops.connected.enums import DatasetSourceType
from datarobot.mlops.connected.enums import HTTPStatus
from datarobot.mlops.connected.url_helper import MMMEndpoint
from datarobot.mlops.constants import Constants
from datarobot.mlops.json_shim import default_serializer
from datarobot.mlops.json_shim import json_dumps_bytes
from datarobot.mlops.metric import AggregatedStats
from datarobot.mlops.metric import DeploymentStats
from datarobot.mlops.metric import DeploymentStatsContainer
from datarobot.mlops.metric import GeneralStats
from datarobot.mlops.metric import PredictionsData
from datarobot.mlops.metric import PredictionsDataContainer
from datarobot.mlops.metric import SerializationConstants

from .exception import DRMLOpsConnectedException
from .url_helper import URLBuilder

logger = logging.getLogger(__name__)


class MMMLimits:
    DATA_REPORTING_MAX_CHUNKS = 100
    DATA_REPORTING_MAX_LINES_PER_CHUNK = 100
    ACTUALS_REPORTING_MAX_LINES = 10000


agg_stats_data_keys = SerializationConstants.AggregatedStatsConstants
predictions_data_keys = SerializationConstants.PredictionsDataConstants
common_fields_keys = SerializationConstants.GeneralConstants


class DataRobotAppVersion(object):
    def __init__(self, string_version=None, major=None, minor=None, patch=None):
        if string_version is not None:
            versions = string_version.split(".")
            if len(versions) < 3:
                raise ValueError(
                    "DataRobot App version in string form should have syntax \"x.y.z\" "
                    "where x, y and z are integers"
                )
            major = versions[0]
            minor = versions[1]
            patch = versions[2]
        elif major is None or minor is None or patch is None:
            raise ValueError(
                "DataRobot App version needs to be specified either as a string \"x.y.z\" "
                "or integer values for major, minor, patch"
            )

        self._major = int(major)
        self._minor = int(minor)
        self._patch = int(patch)

    def __str__(self):
        return "{}.{}.{}".format(self._major, self._minor, self._patch)

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    def is_newer_or_equal(self, datarobot_app_compare_version):
        """
        Checks if "this" version is newer or equal to the version input as an argument
        :param datarobot_app_compare_version:
        :return:
        """
        if self._major > datarobot_app_compare_version.major:
            return True
        if self._major < datarobot_app_compare_version.major:
            return False
        # At this point major versions are equal
        if self._minor > datarobot_app_compare_version.minor:
            return True
        if self._minor < datarobot_app_compare_version.minor:
            return False
        # At this point major and minor versions are equal
        return self._patch >= datarobot_app_compare_version.patch


DATAROBOT_APP_VERSION_WITH_SKIP_AGGREGATION_SUPPORT = DataRobotAppVersion(major=8, minor=0, patch=6)


class MLOpsClient(object):
    """
    This class provides helper methods to communicate with
    DataRobot MLOps.
    *Note*: These class methods can only be run from a node
    with connectivity to DataRobot MLOps.

    :param service_url: DataRobot MLOps URL
    :type service_url: str
    :param api_key: DataRobot MLOps user API key
    :type api_key: str
    :returns: class instance
    :rtype: MLOpsClient
    """

    AUTHORIZATION_TOKEN_PREFIX = "Bearer "
    RESPONSE_PREDICTION_ENVIRONMENT_ID_KEY = "id"
    RESPONSE_DEPLOYMENT_ID_KEY = "id"
    RESPONSE_MODEL_PACKAGE_ID_KEY = "id"
    RESPONSE_MODEL_ID_KEY = "modelId"
    RESPONSE_CATALOG_ID_KEY = "catalogId"
    RESPONSE_STATUS_KEY = "status"
    RESPONSE_MODEL_KEY = "model"
    RESPONSE_MODEL_PACKAGE_KEY = "modelPackage"
    RESPONSE_DATA_INFO_KEY = "externalDataInfo"
    RESPONSE_TARGET_KEY = "target"
    RESPONSE_TARGET_TYPE_KEY = "type"
    RESPONSE_MODEL_TARGET_TYPE_KEY = "targetType"
    RESPONSE_LOCATION_KEY = "Location"
    RESPONSE_FULL_API_VERSION = "versionString"
    RESPONSE_API_MAJOR_VERSION = "major"
    RESPONSE_API_MINOR_VERSION = "minor"

    ASYNC_STATUS_ACTIVE = "active"
    ASYNC_STATUS_ERROR = "error"
    ASYNC_STATUS_ABORT = "abort"
    ASYNC_STATUS_INITIALIZED = "initialized"
    ASYNC_STATUS_RUNNING = "running"
    ASYNC_WAIT_SLEEP_TIME = 2

    # match the target type strings in API payloads and responses
    TARGET_TYPE_BINARY = "Binary"
    TARGET_TYPE_REGRESSION = "Regression"
    TARGET_TYPE_MULTICLASS = "Multiclass"

    def __init__(
        self, service_url, api_key, verify=True, dry_run=False, datarobot_app_version=None
    ):
        self._service_url = service_url
        self._api_key = MLOpsClient.AUTHORIZATION_TOKEN_PREFIX + api_key
        self._verify = verify
        self._common_headers = {"Authorization": self._api_key}
        self._api_version = None
        self._api_major_version = None
        self._api_minor_version = None
        self._url_builder = URLBuilder(self._service_url)
        self.__session = None

        if dry_run:
            return

        self.update_api_version()
        self.update_datarobot_app_version()

        # If the DataRobot App Version is not input, we use the current MLOps library version
        # This is because, "typically", for every DataRobot App release, we have a corresponding
        # MLOps package release
        if datarobot_app_version:
            self._datarobot_app_version = DataRobotAppVersion(string_version=datarobot_app_version)
        else:
            self._datarobot_app_version = DataRobotAppVersion(
                string_version=Constants.MLOPS_VERSION
            )

        major = 2
        minor = 18
        error = (
            "Tracking Agent can work with DataRobot API version '{}.{}' and above."
            "Current version: {} is old.".format(major, minor, self._api_version)
        )

        if self.is_api_version_older_than(2, 18):
            raise DRMLOpsConnectedException(error)

        if not self._verify:
            logger.warning("SSL certificates will not be verified.")

    def is_api_version_older_than(self, reference_major_version, reference_minor_version):
        if self._api_major_version < reference_major_version:
            return True
        return (
            self._api_major_version == reference_major_version
            and self._api_minor_version < reference_minor_version
        )

    @property
    def _session(self):
        # Lazily create the ClientSession so users don't have to remember to call shutdown()
        # if they didn't actually end up needing an async client.
        if self.__session is None:
            self.__session = aiohttp.ClientSession()
        return self.__session

    def _wait_for_async_completion(self, async_location, max_wait):
        """
        Wait for successful resolution of the provided async_location.

        :param async_location: The URL we are polling for resolution.
        :type async_location: str
        :param max_wait: The number of seconds to wait before giving up.
        :type max_wait: int
        :returns: True on success.
        :rtype: bool
        :returns: The URL of the now-finished resource
        :rtype str
        :raises: DRMLOpsConnectedException if status is error
        :raises: RuntimeError if the resource did not resolve in time
        """
        start_time = time.time()

        while time.time() < start_time + max_wait:
            response = self._get_url_request_response(async_location, allow_redirects=False)
            if response.status_code == HTTPStatus.SEE_OTHER:
                return response.headers[MLOpsClient.RESPONSE_LOCATION_KEY]
            if response.status_code != HTTPStatus.OK:
                raise DRMLOpsConnectedException(
                    "Call {} failed; text: [{}]".format(async_location, response.text)
                )
            data = response.json()
            if MLOpsClient.RESPONSE_STATUS_KEY in data:
                async_status = data[MLOpsClient.RESPONSE_STATUS_KEY].lower()
                if async_status in [
                    MLOpsClient.ASYNC_STATUS_INITIALIZED,
                    MLOpsClient.ASYNC_STATUS_RUNNING,
                ]:
                    pass
                elif async_status in [MLOpsClient.ASYNC_STATUS_ACTIVE]:
                    return True
                elif async_status in [
                    MLOpsClient.ASYNC_STATUS_ABORT,
                    MLOpsClient.ASYNC_STATUS_ERROR,
                ]:
                    raise DRMLOpsConnectedException(str(data))
                else:
                    raise DRMLOpsConnectedException(
                        "Task status '{}' is not valid".format(async_status)
                    )
            else:
                return True
            logger.debug(
                "Retrying request to %s in %s seconds.",
                async_location,
                MLOpsClient.ASYNC_WAIT_SLEEP_TIME,
            )
            time.sleep(MLOpsClient.ASYNC_WAIT_SLEEP_TIME)
        raise RuntimeError("Client timed out waiting for {} to resolve".format(async_location))

    def update_api_version(self):
        url = self._service_url + "/" + MMMEndpoint.API_VERSION
        headers = dict(self._common_headers)
        try:
            response = requests.get(url, headers=headers, verify=self._verify)
            if response.ok:
                self._api_version = response.json()[MLOpsClient.RESPONSE_FULL_API_VERSION]
                self._api_major_version = response.json()[MLOpsClient.RESPONSE_API_MAJOR_VERSION]
                self._api_minor_version = response.json()[MLOpsClient.RESPONSE_API_MINOR_VERSION]
            else:
                if "invalid authorization header" in response.text.lower():
                    raise DRMLOpsConnectedException(
                        "Call {} failed: invalid Authorization header. "
                        "Make sure you have supplied a valid API token.".format(url)
                    )
                raise DRMLOpsConnectedException(
                    "Call {} failed; text: [{}]".format(url, response.text)
                )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def update_datarobot_app_version(self):
        """
        Placeholder method to query the DataRobot App version if and when it is available
        :return:
        """
        return

    def delete_deployment(self, deployment_id, wait_for_result=False, force=False, timeout=300):
        """
        Delete the deployment with the provided ID.

        :param deployment_id: ID of the deployment to delete
        :type deployment_id: str
        :param wait_for_result: if True, wait for operation to finish. If False, return immediately.
        :type wait_for_result: bool
        :param timeout: if wait_for_result is True, how long to wait for async completion
        :type timeout: int
        :returns void
        :raises DRMLOpsConnectedException: if the deployment does not exist, user does not have
        permission to delete, or the deployment is in use by an application
        """
        try:
            url = self._url_builder.deployment(deployment_id, force)
            response = requests.delete(url, headers=self._common_headers, verify=self._verify)

            # status code is:
            # NO_CONTENT when deployment is deleted
            # GONE when deployment was previously deleted
            # NOT_FOUND if deployment was already deleted or user has no permission to delete
            # 422 if an application is currently associated with the deployment
            if response.status_code in [HTTPStatus.NO_CONTENT]:
                return
            if response.status_code == HTTPStatus.ACCEPTED:
                if wait_for_result:
                    logger.info(
                        "Waiting up to {} seconds for operation to complete...".format(timeout)
                    )
                    self._wait_for_async_completion(
                        response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
                    )
                return
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            if response.status_code == HTTPStatus.IN_USE:
                raise DRMLOpsConnectedException(
                    "Call {} failed; deployment ID {} in use.".format(url, deployment_id)
                )
            raise DRMLOpsConnectedException(
                "Call {} failed; unexpected status code: {}; text:[{}]".format(
                    url, response.status_code, response.text
                )
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def upload_dataset(self, dataset_filepath, timeout=180, dry_run=False):
        """
        Upload a dataset (from a CSV file) into DataRobot MLOps

        :param dataset_filepath: path to a CSV dataset file
        :type dataset_filepath: str
        :param timeout: time in seconds to wait for result (default is 180 seconds)
        :type timeout: int
        :returns: dataset ID
        :rtype: str
        :raises DRMLOpsConnectedException: if dataset upload failed
        """

        try:
            url = self._url_builder.upload_dataset()
            headers = dict(self._common_headers)
            if dry_run:
                return "dummy-catalog-id-dry-run"
            with open(dataset_filepath) as dataset_file:
                response = requests.post(
                    url,
                    files={"file": (dataset_filepath, dataset_file)},
                    headers=headers,
                    verify=self._verify,
                )
                if response.ok:
                    self._wait_for_async_completion(
                        response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
                    )
                    return response.json()[MLOpsClient.RESPONSE_CATALOG_ID_KEY]
                else:
                    raise DRMLOpsConnectedException(
                        "Call {} with filename {} failed; text:[{}]".format(
                            url, dataset_filepath, response.text
                        )
                    )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def upload_dataframe(self, df, filename=None, timeout=180, dry_run=False):
        """
        Upload a DataFrame to MLOps.  Internally, a DataFrame is serialized to CSV and then
        uploaded to AI Catalog.  Filename is used just as display name; no actual file is created.

        :param df: input DataFrame to upload
        :type df: pandas.Dataframe
        :param filename: Filename string used as display name in "AI Catalog"
        :type filename: str
        :param timeout: time in seconds to wait for result (default is 180 seconds)
        :type timeout: int
        :returns: dataset ID
        :rtype: str
        :raises DRMLOpsConnectedException: if dataset upload failed
        """

        try:
            url = self._url_builder.upload_dataset()
            headers = dict(self._common_headers)
            if dry_run:
                return "dummy-catalog-id-dry-run"

            if filename:
                file_meta = (filename, df.to_csv(index=False))
            else:
                file_meta = df.to_csv(index=False)
            response = requests.post(
                url, files={"file": file_meta}, headers=headers, verify=self._verify
            )
            if response.ok:
                self._wait_for_async_completion(
                    response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
                )
                return response.json()[MLOpsClient.RESPONSE_CATALOG_ID_KEY]
            else:
                raise DRMLOpsConnectedException(
                    "Call {} for DataFrame failed; text:[{}]".format(url, response.text)
                )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def _get_url_request_response(self, url, allow_redirects=True, params=None):
        return requests.get(
            url,
            headers=self._common_headers,
            allow_redirects=allow_redirects,
            verify=self._verify,
            params=params,
        )

    def api_version_smaller_than(self, major, minor):
        if self._api_major_version < major:
            return True

        if self._api_major_version == major and self._api_minor_version < minor:
            return True

        return False

    def associate_deployment_dataset(
        self, deployment_id, dataset_id, data_source_type, timeout=180, dry_run=False
    ):
        """
        Associate a dataset with a deployment in DataRobot MLOps

        :param deployment_id: deployment ID
        :type deployment_id: str
        :param dataset_id: dataset ID
        :type dataset_id: str
        :param data_source_type: dataset type
        :type data_source_type: DatasetSourceType
        :param timeout: time in seconds to wait for result (default is 180 seconds)
        :type timeout: int
        :returns: True if association succeeded
        :raises DRUnsupportedType: if data source type is not supported
        :raises DRMLOpsConnectedException: if association failed
        """

        if not isinstance(data_source_type, DatasetSourceType):
            raise DRUnsupportedType(
                "data_source_type must be of type '{}'".format(DatasetSourceType)
            )

        if data_source_type == DatasetSourceType.TRAINING:
            raise DRMLOpsConnectedException(
                "Associating training data with deployments is not allowed. "
                "Instead associate training data with the model package."
            )

        if data_source_type != DatasetSourceType.SCORING:
            raise DRMLOpsConnectedException(
                "Invalid data source type '{}'".format(data_source_type)
            )

        payload = {
            "datasetId": dataset_id,
        }
        url = self._url_builder.associate_deployment_dataset(deployment_id)

        headers = dict(self._common_headers)
        headers.update({"Content-Type": "application/json"})
        data = json_dumps_bytes(payload)

        try:
            if dry_run:
                return True
            response = requests.post(url, data=data, headers=headers, verify=self._verify)
            if response.ok:
                if self.api_version_smaller_than(2, 23):
                    self._wait_for_async_completion(
                        response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
                    )
                # API responds with HTTP 202, but no longer provides a location header
                return True
            # TODO: verify that the NOT_FOUND applies to the deployment_id only,
            #       so as not to confuse if deployment_id is valid but model_package_id is not
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException(
                "Call {} with payload {} failed; text: [{}]".format(url, payload, response.text)
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_deployment(self, deployment_id):
        """
        Get deployment

        :param deployment_id: deployment ID
        :type deployment_id: str
        :returns: json of deployment info
        :rtype: str
        :raises DRMLOpsConnectedException: if request fails
        """
        try:
            url = self._url_builder.deployment(deployment_id)
            response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def list_deployments(self, params=None):
        url = self._url_builder.list_deployments()
        return self._make_list_call(url, params)

    def get_model_id(self, deployment_id):
        """
        Get current model ID for deployment ID.

        :param deployment_id: deployment ID
        :type deployment_id: str
        :returns: model ID
        :rtype: str
        :raises DRMLOpsConnectedException: if request fails
        """
        deployment = self.get_deployment(deployment_id)
        model_package_id = deployment[MLOpsClient.RESPONSE_MODEL_PACKAGE_KEY][
            MLOpsClient.RESPONSE_MODEL_PACKAGE_ID_KEY
        ]
        model_package = self.get_model_package(model_package_id)
        return model_package[MLOpsClient.RESPONSE_MODEL_ID_KEY]

    def get_deployment_type(self, deployment_id):
        """
        Get the type of deployment, for example, 'Binary' or 'Regression'
        :param deployment_id:
        :type deployment_id: str
        :return: type of Deployment
        :rtype: str
        :raises DRMLOpsConnectedException: if request fails
        """
        deployment = self.get_deployment(deployment_id)

        return deployment[MLOpsClient.RESPONSE_MODEL_KEY][
            MLOpsClient.RESPONSE_MODEL_TARGET_TYPE_KEY
        ]

    def get_dataset(self, dataset_id):
        """
        Get dataset by ID

        :param dataset_id: dataset ID
        :type dataset_id: str
        :returns: dataset metadata
        :rtype: str
        :raises DRMLOpsConnectedException: if request fails
        """
        try:
            url = self._url_builder.get_dataset(dataset_id)
            response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Dataset ID {} not found.".format(dataset_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def list_datasets(self, params=None):
        url = self._url_builder.list_datasets()
        return self._make_list_call(url, params)

    def soft_delete_dataset(self, dataset_id):
        """
        Soft delete (mark as deleted) the dataset with the provided ID.

        :param dataset_id: ID of the dataset to delete
        :type dataset_id: str
        :returns None, if dataset has been successfully deleted during this call
        :rtype None
        :raises DRNotFoundException: if dataset doesn't exist (not found or already deleted)
        :raises DRMLOpsConnectedException: call fails for other unexpected reason
        """
        try:
            url = self._url_builder.soft_delete_dataset(dataset_id)
            response = requests.delete(url, headers=self._common_headers, verify=self._verify)

            # status code is:
            # NO_CONTENT when dataset was deleted
            # GONE when dataset was previously deleted
            # NOT_FOUND when dataset with provided DIId has never existed
            if response.status_code == HTTPStatus.NO_CONTENT:
                return
            if response.status_code in [HTTPStatus.GONE, HTTPStatus.NOT_FOUND]:
                raise DRNotFoundException("Dataset ID {} not found.".format(dataset_id))
            raise DRMLOpsConnectedException(
                "Call {} failed; unexpected status code: {}; text:[{}]".format(
                    url, response.status_code, response.text
                )
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def set_scoring_dataset(self, deployment_id, dataset_filepath):
        # TODO: This method is never called. It looks like:
        #           MLOpsCli.upload_dataset calls MLOpsClient.upload_dataset
        #           MLOpsCli.upload_scoring_dataset calls MLOpsClient.associate_deployment_dataset
        #       Should this method exist as a standalone?
        """
        Upload scoring dataset and
        associate it with a deployment in DataRobot MLOps.

        :param deployment_id: deployment ID
        :type deployment_id: str
        :param dataset_filepath: path to a CSV dataset file
        :type dataset_filepath: str
        :returns: dataset ID
        :rtype: str
        """
        dataset_id = self.upload_dataset(dataset_filepath)
        self.associate_deployment_dataset(deployment_id, dataset_id, DatasetSourceType.SCORING)
        return dataset_id

    def submit_actuals(self, deployment_id, actuals, wait_for_result=True, timeout=180):
        """
        :param deployment_id: ID of the deployment for which the actuals are being submitted
        :param actuals: List of actuals with schema:
                        Regression: {"actualValue": 23, "wasActedOn": False / True,
                        "timestamp": RFC3339 timestamp, "associationId": "x_23423_23423"}
                        Binary: {"actualValue": "<className>", "wasActedOn": False / True,
                        "timestamp": RFC3339 timestamp, "associationId": "x_23423_23423"}
        :param wait_for_result: if True, wait for operation to finish. If False, return immediately.
        :type wait_for_result: bool
        :param timeout: if wait_for_result is True, how long to wait for async completion
        :type timeout: int
        """

        if len(actuals) == 0:
            raise DRMLOpsConnectedException("Empty actuals list to post")

        for actual in actuals:
            if Constants.ACTUALS_VALUE_KEY not in actual:
                raise DRMLOpsConnectedException(
                    "'{}' missing in '{}'".format(Constants.ACTUALS_VALUE_KEY, str(actual))
                )
            if (
                not isinstance(actual[Constants.ACTUALS_VALUE_KEY], float)
                and not isinstance(actual[Constants.ACTUALS_VALUE_KEY], str)
                and not isinstance(actual[Constants.ACTUALS_VALUE_KEY], int)
            ):
                raise DRUnsupportedType(
                    "'{}' must be either string, int or float, '{}'".format(
                        Constants.ACTUALS_VALUE_KEY, str(actual)
                    )
                )

            if Constants.ACTUALS_ASSOCIATION_ID_KEY not in actual:
                raise DRMLOpsConnectedException(
                    "'{}' missing in '{}'".format(Constants.ACTUALS_ASSOCIATION_ID_KEY, str(actual))
                )

            if Constants.ACTUALS_WAS_ACTED_ON_KEY in actual and not isinstance(
                actual[Constants.ACTUALS_WAS_ACTED_ON_KEY], bool
            ):
                raise DRUnsupportedType(
                    "'{}' should be bool, '{}'".format(
                        Constants.ACTUALS_WAS_ACTED_ON_KEY, str(actual)
                    )
                )

        url = self._url_builder.report_actuals(deployment_id)
        headers = dict(self._common_headers)
        headers.update({"Content-Type": "application/json"})
        data = {"data": actuals}
        response = requests.post(
            url, headers=headers, data=json_dumps_bytes(data), verify=self._verify
        )
        if response.status_code != HTTPStatus.ACCEPTED:
            raise DRMLOpsConnectedException("Failed to post actuals: {}".format(response.text))
        if wait_for_result:
            self._wait_for_async_completion(
                response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
            )
        return response

    @staticmethod
    def _validate_col_exists(df, col_name):
        if col_name not in df.columns:
            raise Exception("Data does not include {} column".format(col_name))

    @staticmethod
    def _get_correct_actual_value(deployment_type, value):
        if deployment_type == "Regression":
            return float(value)
        return str(value)

    @staticmethod
    def _get_correct_flag_value(value_str):
        if value_str == "True":
            return True
        return False

    def submit_actuals_from_dataframe(
        self,
        deployment_id,
        dataframe,
        assoc_id_col=Constants.ACTUALS_ASSOCIATION_ID_KEY,
        actual_value_col=Constants.ACTUALS_VALUE_KEY,
        was_act_on_col=Constants.ACTUALS_WAS_ACTED_ON_KEY,
        timestamp_col=Constants.ACTUALS_TIMESTAMP_KEY,
        progress_callback=None,
        wait_for_result=True,
        timeout=120,
    ):
        """
        Submit actuals to MLOps App from the given DataFrame.
        This call will specific columns of the DataFrame to extract the association ids,
        actual values of predictions and other information. The data will be submitted to the
        MLOps app chunk by chunk, where the maximal chunk size is 10K lines.

        :param deployment_id: ID of deployment to report actual on
        :type deployment_id: str
        :param dataframe: DataFrame containing all the data
        :type dataframe: pandas.DataFrame
        :param assoc_id_col: Name of column containing the unique id for each prediction
        :type assoc_id_col: str
        :param actual_value_col: Name of column containing the actual value
        :type actual_value_col: str
        :param was_act_on_col: Name of column which indicates if there was an action taken on this
                               prediction
        :type was_act_on_col: str
        :param timestamp_col: Name of column containing a timestamp for the action
        :type timestamp_col: str
        :param progress_callback: A function to call after each chunk is sent to the MLOps App.
         Function signature is:
           progress_callback(total_number_of_actuals,
                             actuals_sent_so_far,
                             time_sending_last_chunk_in_seconds)

        :returns: The status of the last request to submit actuals. see the submit_actuals method
        :raises DRMLOpsConnectedException: If there was an error connecting to the MLOps app.

        """
        # Sanity check that we have all needed columns in our data
        self._validate_col_exists(dataframe, actual_value_col)
        self._validate_col_exists(dataframe, assoc_id_col)

        # Renaming the columns in case the columns needed are not in the expected name
        cols_to_rename = {}
        if assoc_id_col != Constants.ACTUALS_ASSOCIATION_ID_KEY:
            cols_to_rename[assoc_id_col] = Constants.ACTUALS_ASSOCIATION_ID_KEY
        if actual_value_col != Constants.ACTUALS_VALUE_KEY:
            cols_to_rename[actual_value_col] = Constants.ACTUALS_VALUE_KEY
        if was_act_on_col != Constants.ACTUALS_WAS_ACTED_ON_KEY:
            cols_to_rename[was_act_on_col] = Constants.ACTUALS_WAS_ACTED_ON_KEY
        if timestamp_col and timestamp_col != Constants.ACTUALS_TIMESTAMP_KEY:
            cols_to_rename[timestamp_col] = Constants.ACTUALS_TIMESTAMP_KEY
        dataframe = dataframe.rename(columns=cols_to_rename)

        # Taking only the columns we need for the actuals reporting
        cols_to_take = [Constants.ACTUALS_VALUE_KEY, Constants.ACTUALS_ASSOCIATION_ID_KEY]
        if timestamp_col:
            cols_to_take.append(Constants.ACTUALS_TIMESTAMP_KEY)
        if Constants.ACTUALS_WAS_ACTED_ON_KEY in dataframe.columns:
            cols_to_take.append(Constants.ACTUALS_WAS_ACTED_ON_KEY)

        dataframe = dataframe[cols_to_take]
        # ensure the association ID is a string
        dataframe[Constants.ACTUALS_ASSOCIATION_ID_KEY] = dataframe[
            Constants.ACTUALS_ASSOCIATION_ID_KEY
        ].map(str)

        # Iterating over the rows of the DataFrame and building the actuals list of dictionaries
        deployment_type = self.get_deployment_type(deployment_id)
        actuals = []

        request_ret_val = None

        total_number_of_actuals = len(dataframe.index)
        requests_sent = 0
        for index, row in dataframe.iterrows():
            actual = {}
            for key, value in row.items():
                if key == Constants.ACTUALS_WAS_ACTED_ON_KEY:
                    value = self._get_correct_flag_value(value)
                if key == Constants.ACTUALS_VALUE_KEY:
                    value = self._get_correct_actual_value(deployment_type, value)
                actual[key] = value
            actuals.append(actual)
            if len(actuals) == MMMLimits.ACTUALS_REPORTING_MAX_LINES:
                start_time = time.time()
                request_ret_val = self.submit_actuals(
                    deployment_id, actuals, wait_for_result=wait_for_result, timeout=timeout
                )
                end_time = time.time()
                requests_sent += 1
                if progress_callback:
                    progress_callback(
                        total_number_of_actuals,
                        requests_sent * MMMLimits.ACTUALS_REPORTING_MAX_LINES,
                        end_time - start_time,
                    )
                actuals = []
        if len(actuals) > 0:
            start_time = time.time()
            request_ret_val = self.submit_actuals(
                deployment_id, actuals, wait_for_result=wait_for_result, timeout=timeout
            )
            end_time = time.time()
            if progress_callback:
                progress_callback(
                    total_number_of_actuals, total_number_of_actuals, end_time - start_time
                )
        return request_ret_val

    def create_model_package(self, model_info):
        """
        Create an external model package in DataRobot MLOps from JSON configuration

        :param model_info: a JSON object of model parameters
        :type model_info: dict
        :returns: model package ID of newly created model
        :rtype: str
        :raises DRMLOpsConnectedException: if model package creation failed

        Example JSON for a regression model:

        .. sourcecode:: json

            {
              "name": "Lending club regression",
              "modelDescription": {
                "description": "Regression on lending club dataset"
              }
              "target": {
                "type": "Regression",
                "name": "loan_amnt
              }
            }


        Example JSON for a binary classification model:

        .. sourcecode:: json

            {
              "name": "Surgical Model",
              "modelDescription": {
                "description": "Binary classification on surgical dataset",
                "location": "/tmp/myModel"
              },
              "target": {
                 "type": "Binary",
                 "name": "complication",
                 "classNames": ["Yes","No"],  # minority/positive class should be listed first
                 "predictionThreshold": 0.5
                }
            }

        Example JSON for a multiclass classification model:

        .. sourcecode:: json

            {
                "name": "Iris classifier",
                "modelDescription": {
                    "description": "Classification on iris dataset",
                    "location": "/tmp/myModel"
                },
                "target": {
                    "type": "Multiclass",
                    "name": "Species",
                    "classNames": [
                        "Iris-versicolor",
                        "Iris-virginica",
                        "Iris-setosa"
                    ]
                }
            }
        """

        try:
            url = self._url_builder.create_model_package()
            headers = dict(self._common_headers)
            headers.update({"Content-Type": "application/json"})
            response = requests.post(
                url, data=json_dumps_bytes(model_info), headers=headers, verify=self._verify
            )
            if response.ok:
                return response.json()[MLOpsClient.RESPONSE_MODEL_PACKAGE_ID_KEY]
            else:
                raise DRMLOpsConnectedException(
                    "Call {} with payload {} failed; text: [{}]".format(
                        url, model_info, response.text
                    )
                )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_features_from_model_package(self, model_package_id, params=None):
        try:
            url = self._url_builder.features_model_package(model_package_id)
            response = self._get_url_request_response(url, params=params)
            if response.ok:
                return response.json()["data"]
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Model package ID {} not found.".format(model_package_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_model_package(self, model_package_id):
        """
        Get information about a model package from DataRobot MLOps

        :param model_package_id: ID of the model package
        :type model_package_id: str
        :returns: JSON containing the model package metadata
        :rtype: str
        :raises DRMLOpsConnectedException: if model package retrieval failed
        """

        try:
            url = self._url_builder.get_model_package(model_package_id)
            response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Model package ID {} not found.".format(model_package_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def list_model_packages(self, params=None):
        url = self._url_builder.list_model_packages()
        return self._make_list_call(url, params)

    def archive_model_package(self, model_package_id):
        """
        Delete a model package from DataRobot MLOps

        :param model_package_id: ID of the model package
        :type model_package_id: str
        :returns None, if model package has been successfully deleted (archived) during this call
        :rtype None
        :raises DRNotFoundException: if model package doesn't exist (not found or already deleted)
        :raises DRMLOpsConnectedException: call fails for other unexpected reason
        """
        try:
            url = self._url_builder.archive_model_package(model_package_id)
            response = requests.post(url, headers=self._common_headers, verify=self._verify)

            # status code is:
            # NO_CONTENT when model package was deleted
            # GONE when model package was previously deleted
            # NOT_FOUND when model package with provided id has never existed
            if response.status_code == HTTPStatus.NO_CONTENT:
                return
            # treating GONE and NOT_FOUND the same (consistent with deleting other resources)
            if response.status_code in [HTTPStatus.GONE, HTTPStatus.NOT_FOUND]:
                raise DRNotFoundException("Model package ID {} not found.".format(model_package_id))
            raise DRMLOpsConnectedException(
                "Call {} failed; unexpected status code: {}; text:[{}]".format(
                    url, response.status_code, response.text
                )
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def deploy_model_package(
        self,
        model_package_id,
        label,
        description="",
        wait_for_result=True,
        timeout=180,
        prediction_environment_id=None,
    ):
        """
        Create a new deployment for the model package.

        :param model_package_id: ID of the model package
        :type model_package_id: str
        :param label: label for this deployment
        :type label: str
        :param description: description for this deployment
        :type description: str
        :param wait_for_result: if True, wait for operation to finish. If False, return immediately.
        :type wait_for_result: bool
        :param timeout: if wait_for_result is True, how long to wait for async completion
        :type timeout: int
        :param prediction_environment_id: ID of prediction environment to deploy to
        :type prediction_environment_id: str
        :return: deployment ID of the new deployment
        :rtype: str
        :raises DRMLOpsConnectedException: if deployment fails
        """

        deployment_info = {
            "modelPackageId": model_package_id,
            "label": label,
            "description": description,
        }
        if prediction_environment_id:
            deployment_info["predictionEnvironmentId"] = prediction_environment_id

        try:
            url = self._url_builder.deploy_model_package()

            headers = dict(self._common_headers)
            headers.update({"Content-Type": "application/json"})
            response = requests.post(
                url, data=json_dumps_bytes(deployment_info), headers=headers, verify=self._verify
            )
            if response.ok:
                deployment_id = response.json()[MLOpsClient.RESPONSE_DEPLOYMENT_ID_KEY]
                if wait_for_result:
                    self._wait_for_async_completion(
                        response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
                    )
                return deployment_id
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Model package ID {} not found.".format(model_package_id))
            raise DRMLOpsConnectedException(
                "Call {} with payload {} failed; text: [{}]".format(
                    url, deployment_info, response.text
                )
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def replace_model_package(self, deployment_id, model_package_id, reason, timeout=180):
        """
        Replace the model on the deployment

        :param deployment_id: ID of the deployment
        :type model_package_id: str
        :param model_package_id: ID of the new model package
        :type model_package_id: str
        :param reason: reason for replacement. One of "ACCURACY", "DATA_DRIFT",
                       "ERRORS", "SCHEDULED_REFRESH", "SCORING_SPEED", or "OTHER"
        :param timeout: time in seconds to wait for result (default is 180 seconds)
        :type timeout: int
        :return: void
        :raises DRMLOpsConnectedException: if model replacement fails
        """

        replacement_info = {"modelPackageId": model_package_id, "reason": reason}

        try:
            url = self._url_builder.replace_model_package(deployment_id)
            headers = dict(self._common_headers)
            headers.update({"Content-Type": "application/json"})

            response = requests.patch(
                url, data=json_dumps_bytes(replacement_info), headers=headers, verify=self._verify
            )
            if response.ok:
                self._wait_for_async_completion(
                    response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
                )
                return
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException(
                "Call {} with deployment ID {} and model package ID {} failed; text:[{}]".format(
                    url, deployment_id, model_package_id, response.text
                )
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def update_deployment_settings(
        self,
        deployment_id,
        target_drift,
        feature_drift,
        segment_attributes=None,
        timeout=180,
        timestamp_col_name=None,
        timestamp_format=None,
        batch_monitoring=False,
    ):
        """
        Update deployment settings

        :param deployment_id: deployment ID
        :type deployment_id: str
        :param target_drift: whether to enable target drift
        :type target_drift: bool
        :param feature_drift: whether to enable feature drift
        :type feature_drift: bool
        :param segment_attributes: comma-separated segment names, for segment attr analysis
        :type segment_attributes: str
        :param timeout: time in seconds to wait for result (default is 180 seconds)
        :type timeout: int
        :param timestamp_col_name: name of the timestamp column
        :type timestamp_col_name: str
        :param timestamp_format: format of the timestamp column values
        :type timestamp_format: str
        :param batch_monitoring: whether to enable batch monitoring
        :type batch_monitoring: bool
        :returns: void
        """

        target_drift_json = {"enabled": target_drift}
        feature_drift_json = {"enabled": feature_drift}

        settings_info = {
            "targetDrift": target_drift_json,
            "featureDrift": feature_drift_json,
        }

        if batch_monitoring:
            settings_info["batchMonitoring"] = {"enabled": batch_monitoring}

        if timestamp_col_name is not None and timestamp_format is not None:
            predictions_by_forecast_date = {
                "enabled": True,
                "columnName": timestamp_col_name,
                "datetimeFormat": timestamp_format,
            }
            settings_info["predictionsByForecastDate"] = predictions_by_forecast_date

        if segment_attributes:
            segment_names = [s.strip() for s in segment_attributes.split(",")]
            settings_info["segmentAnalysis"] = {"enabled": True, "attributes": segment_names}

        try:
            url = self._url_builder.deployment_settings(deployment_id)
            headers = dict(self._common_headers)
            headers.update({"Content-Type": "application/json"})

            response = requests.patch(
                url, data=json_dumps_bytes(settings_info), headers=headers, verify=self._verify
            )
            if response.ok:
                self._wait_for_async_completion(
                    response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
                )
                return
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException(
                "Call {} with deployment ID {} and deployment settings {} failed; text:[{}]".format(
                    url, deployment_id, settings_info, response.text
                )
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_deployment_settings(self, deployment_id):
        """
        Get information about a deployment from DataRobot MLOps.

        :param deployment_id: ID of the deployment
        :type deployment_id: str
        :returns: JSON containing the deployment settings metadata
        :rtype: str
        :raises DRMLOpsConnectedException: if deployment info retrieval failed
        """

        try:
            url = self._url_builder.deployment_settings(deployment_id)
            response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def create_prediction_environment(self, pe_info):
        """
        Create an external prediction environment in DataRobot MLOps from JSON configuration.

        :param pe_info: a JSON object of prediction environment parameters
        :type pe_info: dict
        :returns: prediction environment ID of newly created prediction environment
        :rtype: str
        :raises DRMLOpsConnectedException: if creation failed

        Example JSON:

        .. sourcecode:: json

            {
              "name": "Prediction Environment Name",
              "description": "Environment used for developing new models",
              "platform": "Other",
              "supportedModelFormats": ["external"]
            }

        """

        try:
            missing_keys = []
            for key in ["name", "platform", "supportedModelFormats"]:
                try:
                    _ = pe_info[key]
                except KeyError:
                    missing_keys.append(key)
            if len(missing_keys) > 0:
                raise DRMLOpsConnectedException(
                    "create_prediction_environment(): payload is missing {}".format(missing_keys)
                )

            url = self._url_builder.create_prediction_environment()

            headers = dict(self._common_headers)
            headers.update({"Content-Type": "application/json"})
            response = requests.post(
                url, data=json_dumps_bytes(pe_info), headers=headers, verify=self._verify
            )
            if response.ok:
                return response.json()[MLOpsClient.RESPONSE_PREDICTION_ENVIRONMENT_ID_KEY]
            else:
                raise DRMLOpsConnectedException(
                    "Call {} with payload {} failed; text: [{}]".format(url, pe_info, response.text)
                )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_prediction_environment(self, prediction_environment_id):
        """
        Get information about a prediction environment from DataRobot MLOps.

        :param prediction_environment_id: ID of the prediction environment
        :type prediction_environment_id: str
        :returns: JSON containing the prediction environment metadata
        :rtype: str
        :raises DRMLOpsConnectedException: if prediction environment retrieval failed
        """

        try:
            url = self._url_builder.get_prediction_environment(prediction_environment_id)
            response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException(
                    "Prediction environment ID {} not found.".format(prediction_environment_id)
                )
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def _make_list_call(self, url, params=None):
        try:
            response = self._get_url_request_response(url, params=params)
            if response.ok:
                return response.json()["data"]
            else:
                raise DRMLOpsConnectedException(
                    "Call {} failed; text: [{}]".format(url, response.text)
                )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def list_prediction_environments(self, params=None):
        url = self._url_builder.list_prediction_environments()
        return self._make_list_call(url, params)

    def delete_prediction_environment(self, prediction_environment_id):
        """
        Delete the prediction environment with the provided ID.

        :param prediction_environment_id: ID of the prediction environment to delete
        :type prediction_environment_id: str
        :returns None, if prediction environment has been successfully deleted during this call
        :rtype None
        :raises DRNotFoundException: if PE doesn't exist (not found or already deleted)
        :raises DRMLOpsConnectedException: if user does not have permission to delete, or the
        prediction environment is in use by a deployment
        """
        try:
            url = self._url_builder.get_prediction_environment(prediction_environment_id)
            response = requests.delete(url, headers=self._common_headers, verify=self._verify)

            # status code is:
            # NO_CONTENT when prediction environment is deleted
            # GONE if it was previously deleted
            # NOT_FOUND if PE was already deleted or user has no permission to delete
            # 422 if a deployment is currently associated with the PE
            if response.status_code == HTTPStatus.NO_CONTENT:
                return
            if response.status_code in [HTTPStatus.GONE, HTTPStatus.NOT_FOUND]:
                raise DRNotFoundException(
                    "Prediction environment ID {} not found.".format(prediction_environment_id)
                )
            if response.status_code == HTTPStatus.IN_USE:
                raise DRMLOpsConnectedException(
                    "Prediction environment ID {} in use.".format(prediction_environment_id)
                )
            raise DRMLOpsConnectedException(
                "Call {} failed; unexpected status code: {}; text:[{}]".format(
                    url, response.status_code, response.text
                )
            )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def payload_report_deployment_stats(
        self, model_id, timestamp, num_predictions, execution_time_ms=None, batch_name=None
    ):
        deployment_stats = DeploymentStats(num_predictions, execution_time_ms)
        deployment_stats_container = DeploymentStatsContainer(
            GeneralStats(model_id, timestamp, batch_name), deployment_stats
        )
        data = deployment_stats_container.serialize(DataFormat.JSON)
        payload = {"data": [data]}
        return json_dumps_bytes(payload)

    async def report_deployment_stats(
        self,
        deployment_id,
        model_id,
        num_predictions,
        execution_time_ms=None,
        timestamp=None,
        dry_run=False,
        batch_name=None,
    ):
        url = self._url_builder.report_deployment_stats(deployment_id)
        headers = dict(self._common_headers)
        headers.update({"Content-Type": "application/json"})
        payload = self.payload_report_deployment_stats(
            model_id, timestamp, num_predictions, execution_time_ms, batch_name
        )

        try:
            if dry_run:
                return {"message": "ok"}
            else:
                response = await self._session.post(
                    url, headers=headers, data=payload, verify_ssl=self._verify
                )
                if response.status == HTTPStatus.NOT_FOUND:
                    raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
                if response.status != HTTPStatus.ACCEPTED:
                    message = await response.text()
                    raise DRMLOpsConnectedException(
                        "Failed to post deployment stats: {}".format(message)
                    )
                if response.ok:
                    json_response = await response.json()
                    return json_response
                message = await response.text()
                raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, message))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def payload_report_prediction_data(
        self,
        model_id,
        data,
        association_ids=None,
        assoc_id=None,
        predictions=None,
        target_col=None,
        prediction_cols=None,
        class_names=None,
        timestamp=None,
        skip_drift_tracking=False,
        skip_accuracy_tracking=False,
        batch_name=None,
    ):
        """
        Builds the payload to report to MLOps

        Association ids can be passed using 'association_ids' parameter or as part of 'data'
        DataFrame and passing column name in 'assoc_id'.  If both are specified,
        'association_ids' is used.

        Similarly, predictions can be passed using 'predictions' parameter or as part of 'data'
        DataFrame and passing column name in 'target_col'.  If both are specified,
        'predictions' is used

        :param model_id:
        :param data:
        :param association_ids:
        :param assoc_id:
        :param predictions:
        :param target_col:
        :param prediction_cols:
        :param class_names:
        :param timestamp:
        :param skip_drift_tracking:
        :param skip_accuracy_tracking:
        :param batch_name:
        :return:
        """

        predictions = get_predictions(
            df=data,
            predictions=predictions,
            target_col=target_col,
            prediction_cols=prediction_cols,
            class_names=class_names,
        )

        # For 6.0 we should not drop the column
        if self._api_version == "2.20":
            feature_data = data
        else:
            if target_col is not None and target_col in data.columns:
                feature_data = data.drop(columns=target_col)
            else:
                feature_data = data

        assoc_id_list = None
        if association_ids is not None:
            assoc_id_list = association_ids
        elif assoc_id:
            if assoc_id not in feature_data.columns:
                raise Exception(
                    "Error: assoc_id column '{}' is not present in DataFrame".format(assoc_id)
                )
            assoc_ids = feature_data[assoc_id].tolist()
            assoc_id_list = list(map(str, assoc_ids))

        if assoc_id is not None and assoc_id in feature_data.columns:
            feature_data = feature_data.drop(columns=assoc_id)

        nr_lines = len(data)
        max_lines_per_chunk = get_config_default(
            ConfigConstants.MLOPS_SAMPLES_GROUP_SIZE_FOR_MLOPS_API_ENDPOINT,
            MMMLimits.DATA_REPORTING_MAX_LINES_PER_CHUNK,
        )
        nr_chunks = math.ceil(nr_lines / max_lines_per_chunk)
        max_chunks = get_config_default(
            ConfigConstants.MLOPS_MAX_GROUPS_FOR_MLOPS_API_ENDPOINT,
            MMMLimits.DATA_REPORTING_MAX_CHUNKS,
        )
        if nr_chunks > max_chunks:
            raise Exception(
                "The dataset provided for data reporting is too big. Currently supporting "
                " up to {} samples per MLOps API call".format(max_lines_per_chunk * max_chunks)
            )
        payload = []
        for chunk_idx in range(0, nr_chunks):
            from_line = chunk_idx * max_lines_per_chunk
            to_line = (chunk_idx + 1) * max_lines_per_chunk
            if to_line > nr_lines:
                to_line = nr_lines

            assoc_id_list_section = None
            if assoc_id_list:
                assoc_id_list_section = assoc_id_list[from_line:to_line]
            features_df = None
            if len(feature_data.columns) > 0:
                features_df = feature_data[from_line:to_line]
            predictions_data = PredictionsData(
                features_df,
                predictions[from_line:to_line],
                association_ids=assoc_id_list_section,
                class_names=class_names,
            )

            if batch_name and self.is_api_version_older_than(2, 30):
                print(
                    "Current API version: '{}' does not support batch monitoring, it is supported"
                    "from API version '2.30', ignoring batch_name: {}".format(
                        self._api_version, batch_name
                    )
                )
                batch_name = None
            predictions_data_container = PredictionsDataContainer(
                GeneralStats(model_id, timestamp, batch_name=batch_name), predictions_data
            )
            chunk_payload = predictions_data_container.serialize(DataFormat.JSON)

            # Fix the feature part of the payload to be like what MLOps App expects and not
            # what the spooler record expects
            if SerializationConstants.PredictionsDataConstants.FEATURES_FIELD_NAME in chunk_payload:
                features_dict = chunk_payload[
                    SerializationConstants.PredictionsDataConstants.FEATURES_FIELD_NAME
                ]
                dr_fmt_feature_list = []
                for feature in features_dict:
                    dr_fmt_feature_list.append({"name": feature, "values": features_dict[feature]})

                chunk_payload[
                    SerializationConstants.PredictionsDataConstants.FEATURES_FIELD_NAME
                ] = dr_fmt_feature_list
            payload.append(chunk_payload)
        final_request = {"data": payload}
        if self._datarobot_app_version.is_newer_or_equal(
            DATAROBOT_APP_VERSION_WITH_SKIP_AGGREGATION_SUPPORT
        ):
            final_request["skipDriftTracking"] = skip_drift_tracking
            final_request["skipAccuracyTracking"] = skip_accuracy_tracking
        else:
            print(
                "Current DataRobot App version: '{current_version}' is older than the version "
                "which supports skip aggregation feature: '{supported_version}', current skip "
                "aggregation flags (Skip Drift: {skip_drift}, Skip Accuracy: {skip_accuracy}) "
                "will be ignored.".format(
                    current_version=str(self._datarobot_app_version),
                    supported_version=str(DATAROBOT_APP_VERSION_WITH_SKIP_AGGREGATION_SUPPORT),
                    skip_drift=skip_drift_tracking,
                    skip_accuracy=skip_accuracy_tracking,
                )
            )
        return final_request

    async def report_prediction_data(
        self,
        deployment_id,
        model_id,
        data,
        association_ids=None,
        assoc_id_col=None,
        predictions=None,
        target_col=None,
        prediction_cols=None,
        class_names=None,
        timestamp=None,
        skip_drift_tracking=False,
        skip_accuracy_tracking=False,
        batch_name=None,
        dry_run=False,
    ):
        """
        Report prediction data for a given model and deployment

        :param deployment_id: deployment ID to use for reporting
        :type deployment_id: str
        :param model_id: Model ID to report prediction data for
        :type model_id: str
        :param data: DataFrame containing both the feature data and the prediction result
        :type data: pandas.Dataframe
        :param association_ids: List of association ids if not part of the 'data' DataFrame
        :type association_ids: Optional(list(str))
        :param assoc_id_col: Name of column containing association ids
        :type assoc_id_col: Optional(str)
        :param predictions: List of predictions ids if not part of the 'data' DataFrame
        :type predictions: Optional(list(?))
        :param target_col: Name of the target column (label)
        :type target_col: str
        :param prediction_cols: List of names of the prediction columns
        :type prediction_cols: list
        :param class_names: List of target class names
        :type class_names: list
        :param timestamp: RFC3339 Timestamp of this prediction data
        :type timestamp: str
        :param skip_drift_tracking
        :type skip_drift_tracking: bool
        :param skip_accuracy_tracking
        :type skip_accuracy_tracking: bool
        :param batch_name: Name of the batch these predictions belong to
        :type batch_name: str
        :returns: Tuple (response from MLOps, size of payload sent)
        :rtype: Tuple
        :raises DRMLOpsConnectedException: if request fails
        """
        url = self._url_builder.report_prediction_data(deployment_id)
        headers = dict(self._common_headers)
        headers.update({"Content-Type": "application/json"})
        input_row_count = data.shape[0]
        start = 0
        max_lines_per_chunk = get_config_default(
            ConfigConstants.MLOPS_SAMPLES_GROUP_SIZE_FOR_MLOPS_API_ENDPOINT,
            MMMLimits.DATA_REPORTING_MAX_LINES_PER_CHUNK,
        )
        max_chunks = get_config_default(
            ConfigConstants.MLOPS_MAX_GROUPS_FOR_MLOPS_API_ENDPOINT,
            MMMLimits.DATA_REPORTING_MAX_CHUNKS,
        )
        size = max_lines_per_chunk * max_chunks

        aggregate_payload_size = 0
        last_response = {}
        while start < input_row_count:
            end = start + size
            if end > input_row_count:
                end = input_row_count
            data_chunk = data[start:end]
            payload = self.payload_report_prediction_data(
                model_id=model_id,
                data=data_chunk,
                association_ids=association_ids,
                assoc_id=assoc_id_col,
                predictions=predictions,
                prediction_cols=prediction_cols,
                target_col=target_col,
                class_names=class_names,
                timestamp=timestamp,
                skip_drift_tracking=skip_drift_tracking,
                skip_accuracy_tracking=skip_accuracy_tracking,
                batch_name=batch_name,
            )
            payload = json_dumps_bytes(payload, default=default_serializer)
            try:
                if dry_run:
                    payload_size = len(payload)
                    aggregate_payload_size += payload_size
                    start = end
                    last_response = {"message": "ok"}
                else:
                    response = await self._session.post(
                        url, headers=headers, data=payload, verify_ssl=self._verify
                    )
                    # TODO: verify that the NOT_FOUND applies to the deployment_id only, so as
                    #       not to confuse if deployment_id is valid but model_package_id is not
                    if response.status == HTTPStatus.NOT_FOUND:
                        raise DRNotFoundException(
                            "Deployment ID {} not found.".format(deployment_id)
                        )
                    if response.status != HTTPStatus.ACCEPTED:
                        message = await response.text()
                        raise DRMLOpsConnectedException(
                            "Failed to post prediction data: {}".format(message)
                        )
                    if response.ok:
                        json_response = await response.json()
                        last_response = json_response
                        payload_size = len(payload)
                        aggregate_payload_size += payload_size
                        start = end
                    else:
                        message = await response.text()
                        raise DRMLOpsConnectedException(
                            "Call {} failed; text:[{}]".format(url, message)
                        )
                continue

            except requests.exceptions.ConnectionError as e:
                raise DRMLOpsConnectedException(
                    "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
                )

        return last_response, aggregate_payload_size

    def payload_report_aggregated_prediction_data(
        self,
        model_id,
        aggregated_stats,
        timestamp=None,
        batch_name=None,
    ):
        aggregated_stat_object = dict()

        aggregated_stat_object[common_fields_keys.MODEL_ID_FIELD_NAME] = model_id
        if timestamp:
            aggregated_stat_object[common_fields_keys.TIMESTAMP_FIELD_NAME] = timestamp

        if batch_name:
            aggregated_stat_object[common_fields_keys.BATCH_NAME_FIELD_NAME] = batch_name

        if aggregated_stats.get_class_names():
            aggregated_stat_object[
                predictions_data_keys.CLASS_NAMES_FIELD_NAME
            ] = aggregated_stats.get_class_names()

        aggregated_feature_list = convert_aggregated_stats_features_to_dr_format(
            aggregated_stats.get_numeric_aggregate_map(),
            aggregated_stats.get_categorical_aggregate_maps(),
        )
        if len(aggregated_feature_list) > 0:
            aggregated_stat_object[
                predictions_data_keys.FEATURES_FIELD_NAME
            ] = aggregated_feature_list

        predictions_list = convert_aggregated_stats_predictions_to_dr_format(
            aggregated_stats.get_prediction_aggregate_map()
        )
        if len(predictions_list) > 0:
            aggregated_stat_object[predictions_data_keys.PREDICTIONS_FIELD_NAME] = predictions_list

        segment_stat_list = convert_aggregated_stats_segment_attr_to_dr_format(
            aggregated_stats.get_segment_attributes_aggregated_stats()
        )
        if len(segment_stat_list) > 0:
            aggregated_stat_object[
                agg_stats_data_keys.SEGMENT_ATTRIBUTES_FIELD_NAME
            ] = segment_stat_list

        return {"data": [aggregated_stat_object]}

    async def report_aggregated_prediction_data(
        self, deployment_id, model_id, payload=None, batch_name=None, dry_run=False
    ):
        """
        Report aggregated stats data for a given model and deployment

        :param deployment_id: deployment ID to use for reporting
        :type deployment_id: str
        :param model_id: Model ID to report prediction data for
        :type model_id: str
        :param payload: data read from spooler
        :param batch_name: Name of the batch these predictions belong to
        :type batch_name: str
        :param dry_run: if set, record will not be reported to DR app
        :returns: Tuple (response from MLOps, size of payload sent)
        :rtype: Tuple
        :raises DRMLOpsConnectedException: if request fails
        """

        numeric_aggregate_map = payload.get(agg_stats_data_keys.NUMERIC_AGGREGATE_MAP)
        categorical_aggregate_map = payload.get(agg_stats_data_keys.CATEGORICAL_AGGREGATE_MAP)
        prediction_aggregate_map = payload.get(agg_stats_data_keys.PREDICTION_AGGREGATE_MAP)
        segment_attributes_aggregate_stats = payload.get(
            agg_stats_data_keys.SEGMENT_ATTRIBUTES_AGGREGATE_STATS
        )
        class_names = payload.get(predictions_data_keys.CLASS_NAMES_FIELD_NAME)
        timestamp = payload[common_fields_keys.TIMESTAMP_FIELD_NAME]

        url = self._url_builder.report_aggregated_prediction_data(deployment_id)
        headers = dict(self._common_headers)
        headers.update({"Content-Type": "application/json"})

        aggregated_stats = AggregatedStats(
            numeric_aggregate_map=numeric_aggregate_map,
            categorical_aggregate_map=categorical_aggregate_map,
            prediction_aggregate_map=prediction_aggregate_map,
            segment_attributes_aggregated_stats=segment_attributes_aggregate_stats,
            class_names=class_names,
        )

        payload = self.payload_report_aggregated_prediction_data(
            model_id=model_id,
            aggregated_stats=aggregated_stats,
            timestamp=timestamp,
            batch_name=batch_name,
        )
        payload = json_dumps_bytes(payload, default=default_serializer)

        try:
            if dry_run:
                return {"message": "ok"}
            else:
                response = await self._session.post(
                    url, headers=headers, data=payload, verify_ssl=self._verify
                )

                if response.status == HTTPStatus.NOT_FOUND:
                    raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
                if response.status != HTTPStatus.ACCEPTED:
                    message = await response.text()
                    raise DRMLOpsConnectedException(
                        "Failed to post prediction data: {}".format(message)
                    )
                if response.ok:
                    json_response = await response.json()
                    return json_response
                else:
                    message = await response.text()
                    raise DRMLOpsConnectedException(
                        "Call {} failed; text:[{}]".format(url, message)
                    )
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def report_actuals_data(self, deployment_id, actuals, dry_run=False):
        """
        Report actuals data for a given deployment.

        :param deployment_id: deployment ID to use for reporting
        :type deployment_id: str
        :param association_id: association ID of the record
        :type association_id: str
        :param actuals_value: the actual value of a prediction
        :type actuals_value: str
        :param was_acted_on: whether or not the prediction was acted on
        :type was_acted_on: bool
        :param timestamp: RFC3339 Timestamp of this prediction data
        :type timestamp: str

        """
        try:
            if dry_run:
                return {"message": "ok"}
            else:
                self.submit_actuals(deployment_id, actuals)
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def _is_model_package_download_from_registry_supported(self):
        if self._api_major_version > 2:
            return True

        if self._api_major_version == 2 and self._api_minor_version >= 25:
            return True

        return False

    def _download_model(self, output_dir, retrieve_url_response):
        # Write to local file if provided
        _, params = cgi.parse_header(retrieve_url_response.headers.get("Content-Disposition", ""))
        filename = os.path.basename(params["filename"])
        model_package_path = os.path.join(output_dir, filename)
        # Download into a temp file and rename into place when finished because we could have
        # multiple threads trying to download and read into the same destination path and this
        # will make sure we always have a consistent file in place. We need to use the low level
        # mkstemp() because the renaming of the temp file messes with NamedTemporaryFile().
        fd, tmpname = tempfile.mkstemp(dir=output_dir, suffix=".downloading")
        try:
            with os.fdopen(fd, mode="wb") as fh:
                # R/W in chunks so we don't blow up memory for large model pkg files. To get the
                # full benefit, the caller needs to have initiated the download via:
                #   requests.get(..., stream=True)
                for chunk in retrieve_url_response.iter_content(chunk_size=1048576):
                    fh.write(chunk)
            os.replace(tmpname, model_package_path)
        finally:
            with suppress(FileNotFoundError):
                os.unlink(tmpname)
        return model_package_path

    def download_model_package_from_registry(
        self,
        model_package_id,
        output_dir,
        download_scoring_code=False,
        scoring_code_binary=False,
        download_pps_installer=False,
        is_prediction_explanations_supported=False,
        timeout=600,
    ):
        """
        Download the model package file from the model registry

        :param model_package_id: ID of the model package to download
        :param output_dir: destination directory where to download model
        :param download_scoring_code: Download the scoring code "jar" or "mlpkg" file, default is
            mlpkg file
        :param scoring_code_binary: Download scoring code as binary if required
        :param download_pps_installer: Download PPS installer (only for custom models)
        :param is_prediction_explanations_supported: Download JAR with Prediction Explanations
            support
        :param timeout: time to wait for result (sec). Default: 120 sec.
        :return: The path of download model package
        """
        if not self._is_model_package_download_from_registry_supported():
            raise DRMLOpsConnectedException(
                """Downloading model package from model registry is
                supported for API version 2.25 and later"""
            )

        if not os.path.exists(output_dir):
            raise DRMLOpsConnectedException(
                "Provided output_dir '{}' does not exist.".format(output_dir)
            )

        if not os.path.isdir(output_dir):
            raise DRMLOpsConnectedException(
                "Provided output_dir '{}' is not a directory.".format(output_dir)
            )

        headers = dict(self._common_headers)
        params = {"portablePredictionsServerInstaller": "true"} if download_pps_installer else None
        if download_scoring_code and scoring_code_binary:
            # Download binary scoring code in single request
            scoring_code_url = self._url_builder.scoring_code_download_from_registry(
                model_package_id
            )
            response = requests.get(scoring_code_url, headers=headers, verify=self._verify)
            if response.status_code != HTTPStatus.OK:
                raise DRMLOpsConnectedException(
                    "Failed to download binary scoring code: {}".format(response.text)
                )
        else:
            # Wait for completion needed
            if download_scoring_code:
                headers.update({"Content-Type": "application/json"})
                data = json_dumps_bytes(
                    {"includePredictionExplanations": is_prediction_explanations_supported}
                )
                model_build_url = self._url_builder.scoring_code_build_from_registry(
                    model_package_id
                )
                response = requests.post(
                    model_build_url, headers=headers, data=data, verify=self._verify
                )
            else:
                model_build_url = self._url_builder.model_package_build_from_registry(
                    model_package_id
                )
                response = requests.post(
                    model_build_url, headers=headers, params=params, verify=self._verify
                )
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Model package ID {} not found.".format(model_package_id))
            if response.status_code != HTTPStatus.ACCEPTED:
                raise DRMLOpsConnectedException(
                    "Failed to download model package: {}".format(response.text)
                )

            # wait for completion
            model_retrieve_url = self._wait_for_async_completion(
                response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
            )

            # Download the model package
            response = requests.get(
                model_retrieve_url, headers=headers, params=params, stream=True, verify=self._verify
            )
            if response.status_code != HTTPStatus.OK:
                raise DRMLOpsConnectedException(
                    "Failed to download model package: {}".format(response.text)
                )

        return self._download_model(output_dir, response)

    def download_dr_current_model_package(
        self,
        deployment_id,
        output_dir,
        download_scoring_code=False,
        scoring_code_binary=False,
        timeout=600,
    ):
        """
        Download current model package file of given deployment

        :param deployment_id: deployment ID to use for reporting
        :param output_dir: destination directory where to download model
        :param download_scoring_code: Download the scoring code "jar" or "mlpkg" file, default is
            mlpkg file
        :param scoring_code_binary: Download scoring code as binary if required
        :param timeout: time in seconds to wait for result (default is 120 seconds)
        :return: The path of download model package
        """
        if not os.path.exists(output_dir):
            raise DRMLOpsConnectedException(
                "Provided output_dir '{}' does not exist.".format(output_dir)
            )

        if not os.path.isdir(output_dir):
            raise DRMLOpsConnectedException(
                "Provided output_dir '{}' is not a directory.".format(output_dir)
            )

        headers = dict(self._common_headers)
        if download_scoring_code and scoring_code_binary:
            # Download binary scoring code in single request
            scoring_code_url = self._url_builder.scoring_code_download(deployment_id)
            response = requests.get(scoring_code_url, headers=headers, verify=self._verify)
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            if response.status_code != HTTPStatus.OK:
                raise DRMLOpsConnectedException(
                    "Failed to download binary scoring code: {}".format(response.text)
                )
        else:
            # Wait for completion needed
            if download_scoring_code:
                headers.update({"Content-Type": "application/json"})
                data = json_dumps_bytes({"includeAgent": False})
                model_build_url = self._url_builder.scoring_code_build(deployment_id)
                response = requests.post(
                    model_build_url, headers=headers, data=data, verify=self._verify
                )
            else:
                model_build_url = self._url_builder.model_package_build(deployment_id)
                response = requests.post(model_build_url, headers=headers, verify=self._verify)
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            if response.status_code != HTTPStatus.ACCEPTED:
                raise DRMLOpsConnectedException(
                    "Failed to download model package: {}".format(response.text)
                )

            # wait for completion
            model_retrieve_url = self._wait_for_async_completion(
                response.headers[MLOpsClient.RESPONSE_LOCATION_KEY], timeout
            )

            # Download the model package
            response = requests.get(
                model_retrieve_url, headers=headers, stream=True, verify=self._verify
            )
            if response.status_code != HTTPStatus.OK:
                raise DRMLOpsConnectedException(
                    "Failed to download model package: {}".format(response.text)
                )

        return self._download_model(output_dir, response)

    def get_service_stats(self, deployment_id, model_id=None):
        """
        Get information about a deployment's service stats from DataRobot MLOps.

        :param deployment_id: ID of the deployment
        :type deployment_id: str
        :param model_id: (optional) model ID
        :type model_id: str
        :returns: JSON containing the service stats
        :rtype: str
        :raises DRMLOpsConnectedException: if model package retrieval failed
        """
        try:
            url = self._url_builder.get_service_stats(deployment_id)
            if model_id:
                response = self._get_url_request_response(url, params={"modelId": model_id})
            else:
                response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            # TODO: Valid deployment_id with well-formed but invalid (non-existent) model_id does
            #       not return 404 as it should; it returns meaningless output. See MMM-9319.
            if response.status_code == HTTPStatus.NOT_FOUND:
                if (
                    "Model" in response.text
                    and "not found" in response.text
                    and model_id in response.text
                ):
                    raise DRNotFoundException(
                        "Model ID {} not found for deployment ID {}.".format(
                            model_id, deployment_id
                        )
                    )
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_prediction_stats(self, deployment_id, model_id=None):
        """
        Get information about a deployment's prediction stats from DataRobot MLOps.

        :param deployment_id: ID of the deployment
        :type deployment_id: str
        :param model_id: (optional) model ID
        :type model_id: str
        :returns: JSON containing the prediction stats
        :rtype: str
        :raises DRMLOpsConnectedException: if model package retrieval failed.
        """

        # We need to provide the end time for the predictions window.
        # We adjust our window to make sure end is in the future, regardless of timezone.
        # Note: timestamp must obey RFC 3339, so Python's isoformat() is convenient but wrong.
        day_after_tomorrow = datetime.datetime.today() + datetime.timedelta(days=2)
        end_time = datetime.datetime.strftime(day_after_tomorrow, "%Y-%m-%d")

        params = {"end": end_time}
        if model_id:
            params["modelId"] = model_id
        try:
            url = self._url_builder.get_prediction_stats(deployment_id)
            response = self._get_url_request_response(url, params=params)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                if (
                    "Model" in response.text
                    and "not found" in response.text
                    and model_id in response.text
                ):
                    raise DRNotFoundException(
                        "Model ID {} not found for deployment ID {}.".format(
                            model_id, deployment_id
                        )
                    )
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_target_drift(self, deployment_id, model_id=None):
        """
        Get deployment target drift information from DataRobot MLOps.

        :param deployment_id: ID of the deployment
        :type deployment_id: str
        :param model_id: (optional) model ID. Otherwise, use current model.
        :type model_id: str
        :returns: JSON containing the target drift information
        :rtype: str
        :raises DRMLOpsConnectedException: if model package retrieval failed
        """
        try:
            url = self._url_builder.get_target_drift(deployment_id)
            if model_id:
                response = self._get_url_request_response(url, params={"modelId": model_id})
            else:
                response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            # Note: sending a invalid model ID (well-formed but not in deployment model history)
            # results in HTTP 200 but "null" for driftScore, sampleSize, and baselineSampleSize.
            if response.status_code == HTTPStatus.NOT_FOUND:
                if (
                    "Model" in response.text
                    and "not found" in response.text
                    and model_id in response.text
                ):
                    raise DRNotFoundException(
                        "Model ID {} not found for deployment ID {}.".format(
                            model_id, deployment_id
                        )
                    )
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_predictions_and_actuals_stats(self, deployment_id, model_id=None):
        """
        Get information about a deployment's predictions and actuals stats from DataRobot MLOps.

        :param deployment_id: ID of the deployment
        :type deployment_id: str
        :param model_id: (optional) model ID
        :type model_id: str
        :returns: JSON containing the prediction stats
        :rtype: str
        :raises DRMLOpsConnectedException: if model package retrieval failed.
        """
        day_after_tomorrow = datetime.datetime.today() + datetime.timedelta(days=2)
        end_time = datetime.datetime.strftime(day_after_tomorrow, "%Y-%m-%d")

        params = {"end": end_time}
        if model_id:
            params["modelId"] = model_id
        try:
            url = self._url_builder.get_predictions_and_actuals_stats_url(deployment_id)
            response = self._get_url_request_response(url, params=params)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                if (
                    "Model" in response.text
                    and "not found" in response.text
                    and model_id in response.text
                ):
                    raise DRNotFoundException(
                        "Model ID {} not found for deployment ID {}.".format(
                            model_id, deployment_id
                        )
                    )
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_batch_service_statistics(self, deployment_id, batch_id):
        url = self._url_builder.get_batch_service_statistics(deployment_id, batch_id)
        try:
            response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                if "Monitoring batch not found" in response.text:
                    raise DRNotFoundException(
                        "Batch ID {} not found for deployment ID {}.".format(
                            batch_id, deployment_id
                        )
                    )
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def get_batch_data_drift(self, deployment_id, batch_id):
        url = self._url_builder.get_batch_data_drift(deployment_id, batch_id)
        try:
            response = self._get_url_request_response(url)
            if response.ok:
                return response.json()
            if response.status_code == HTTPStatus.NOT_FOUND:
                if "Monitoring batch not found" in response.text:
                    raise DRNotFoundException(
                        "Batch ID {} not found for deployment ID {}.".format(
                            batch_id, deployment_id
                        )
                    )
                raise DRNotFoundException("Deployment ID {} not found.".format(deployment_id))
            raise DRMLOpsConnectedException("Call {} failed; text: [{}]".format(url, response.text))
        except requests.exceptions.ConnectionError as e:
            raise DRMLOpsConnectedException(
                "Connection to DataRobot MLOps [{}] refused: {}".format(self._service_url, e)
            )

    def list_batches(self, deployment_id, params=None):
        url = self._url_builder.list_batches(deployment_id)
        return self._make_list_call(url, params)

    async def shutdown(self):
        if self.__session is not None:
            await self.__session.close()

    def __del__(self):
        if self.__session is not None and not self.__session.closed:
            warnings.warn(
                "Client was not properly shutdown() {}".format(repr(self)),
                ResourceWarning,
            )
