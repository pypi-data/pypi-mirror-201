#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
from abc import ABC, abstractmethod
import copy
import enum
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
)
import time
import requests
from .exception import KaranageException


class KaranageResponse:
    def __init__(
        self, url: str, status: Optional[int] = None, data: Optional[str] = None
    ):
        self.url = url
        self.status = status
        self.data = data


class KaranageConnectionInterface(ABC):
    """Generic connection interface to access to karanage interface.

    :param ABC: Abstraction model class.
    """

    @abstractmethod
    def post(
        self,
        service: str,
        url_offset: Optional[str],
        data: Any = None,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> KaranageResponse:
        """POST request on the server.

        :param service: Service on which we need to access.
        :param url_offset: Offset of the url server.
        :param data: Json data to post, defaults to None.
        :param headers: Headers value to add on the request, defaults to None.
        :param params: Parameters to send on the server, defaults to None.
        :return: Result of the request.
        """

    @abstractmethod
    def get(
        self,
        service: str,
        url_offset: Optional[str],
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> KaranageResponse:
        """GET request on the server.

        :param service: Service on which we need to access.
        :param url_offset: Offset of the url server.
        :param headers: Headers value to add on the request, defaults to None.
        :param params: Parameters to send on the server, defaults to None.
        :return: Result of the request.
        """


class KaranageConnection(KaranageConnectionInterface):
    """Connection on the karanage REST server.

    :param KaranageConnectionInterface: Model of connection.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        group: Optional[str] = None,
        token: Optional[str] = None,
        config_file: Optional[str] = None,
        default_values: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the communication class.
        :param url: URL of the karanage API server.
        :param group: Group of the message (token need to have the autorotation to published on it).
        :param token: Token to validate the access on the application.
        :param config_file: path to the configuration file if overload.
        :param default_values: Default configurations.
        """
        self.url = "http://localhost:20080/karanage/api"
        self.group = "test"
        self.token = None
        # load user default value:
        if default_values is not None:
            if "url" in default_values:
                self.url = default_values["url"]
            if "group" in default_values:
                self.group = default_values["group"]
            if "token" in default_values:
                self.token = default_values["token"]
        # keep correct config file:
        if config_file is None:
            config_file = "/etc/karanage/connection.json"
        # check if the config exist:
        if Path(config_file).exists():
            f = open(config_file, "r")
            configuration = json.loads(f.read())
            f.close()
        else:
            configuration = {}
        # Update data with config file:
        if "url" in configuration:
            self.url = configuration["url"]
        if "group" in configuration:
            self.group = configuration["group"]
        if "token" in configuration:
            self.token = configuration["token"]
        # set user command - line configuration:
        if url is not None:
            self.url = url
        if group is not None:
            self.group = group
        if token is not None:
            self.token = token

    def get_url(self, service: str, url_offset: Optional[str] = None):
        """Get the formatted URL for specific service and specific offset

        :param service: Name of the service we want to connect on.
        :param url_offset: additional url path.
        :return: the specific url string (all before ?).
        """
        if url_offset is None:
            return f"{self.url}/{service}/{self.group}"
        return f"{self.url}/{service}/{self.group}/{url_offset}"

    def update_header(self, headers):
        """Add security header on the client header config.

        :param headers: _description_
        :return: _description_
        """
        if headers is None:
            headers = {}
        else:
            headers = copy.deepcopy(headers)
        if self.token is not None and len(self.token) > 15:
            headers["Authorization"] = f"zota {self.token}"
        return headers

    # @override
    def post(
        self,
        service: str,
        url_offset: Optional[str] = None,
        data: Any = None,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> KaranageResponse:
        headers = self.update_header(headers)
        url = self.get_url(service, url_offset)
        headers["Content-Type"] = "application/json"
        ret = requests.post(url, data=json.dumps(data), headers=headers, params=params)
        try:
            return KaranageResponse(url, ret.status_code, ret.content.decode("utf-8"))
        except requests.exceptions.ConnectionError as ex:
            raise KaranageException(f"Fail connect server: '{url}'", 0, str(ex))

    # @override
    def get(
        self,
        service: str,
        url_offset: Optional[str] = None,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> KaranageResponse:
        headers = self.update_header(headers)
        url = self.get_url(service, url_offset)
        ret = requests.get(url, headers=headers, params=params)
        try:
            return KaranageResponse(url, ret.status_code, ret.content.decode("utf-8"))
        except requests.exceptions.ConnectionError as ex:
            raise KaranageException(f"Fail connect server: '{url}'", 0, str(ex))


class MockData(NamedTuple):
    """Received Mock data from the karanage backend.

    :param NamedTuple: Tuple generic interface
    """
    type: str
    service: str
    url_offset: Optional[str]
    data: Any
    headers: Optional[Dict[str, Any]]
    params: Optional[Dict[str, Any]]


class KaranageMock(KaranageConnectionInterface):
    """Simple Karanage Mock to permit to abstract
    Note: This class is for test only !!!

    :param KaranageConnectionInterface: Model of connection.
    """

    def __init__(
        self,
    ) -> None:
        """Initialize the communication class."""
        self.request: List[MockData] = []

    def post(
        self,
        service: str,
        url_offset: Optional[str],
        data: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> KaranageResponse:
        self.request.append(
            MockData("POST", service, url_offset, data, headers, params)
        )
        return KaranageResponse(f"{service}/{url_offset}", 200, "{}")

    def get(
        self,
        service: str,
        url_offset: Optional[str],
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> KaranageResponse:
        self.request.append(MockData("GET", service, url_offset, None, headers, params))
        return KaranageResponse(f"{service}/{url_offset}", 200, "{}")

    def get_values(self, time_out: Optional[float] = None) -> List[MockData]:
        """get the list of last added values

        :param time_out: Timeout before exiting in error
        :returns: all collected values.
        """
        if time_out is not None and time_out > 0:
            start_time = datetime.now()
            while len(self.request) == 0:
                time.sleep(0.1)
                now = datetime.now()
                if now - start_time > timedelta(seconds=time_out):
                    return []
        out = self.request
        self.request = []
        return out


    def clear_values(self) -> None:
        """Clear all the received data."""
        self.request = []
