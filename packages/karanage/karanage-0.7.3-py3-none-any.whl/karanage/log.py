#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
from datetime import datetime, timezone
import enum
import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import requests

from .connection import KaranageConnectionInterface
from .exception import KaranageException


class GroupLogElement:
    def __init__(self, id: int, data: str, time: Optional[datetime] = None):
        self.id = id
        self.time = time
        self.data = data


## Generic karanage sending system.
class KaranageLog:
    def __init__(
        self, connection: KaranageConnectionInterface, system: Optional[str] = None
    ) -> None:
        """Initialize the communication class.
        :param connection: Connection interface.
        """
        self.connection = connection
        self.system = system
        self.service = "log"

    def send(
        self,
        data: Dict,
        id: Optional[int] = None,
        uuid_group: Optional[int] = None,
        time: Optional[datetime] = None,
    ) -> None:
        """Send a message to the server.
        :param data: Data to send to the server
        :param id: Local internal ID
        :param uuid_group: local internal group UUID
        :param time_log: Receive time of the log
        """
        param: Dict[str, Any] = {}
        if id is not None:
            param["id"] = id
        if uuid_group is not None:
            param["uuid"] = uuid_group
        if time is not None:
            param["time"] = time.astimezone(timezone.utc).isoformat()
        ret = self.connection.post(self.service, self.system, data=data, params=param)
        if ret is None:
            raise KaranageException(
                f"Fail send message sub-library return None")
        if ret.status is None or not 200 <= ret.status <= 299:
            raise KaranageException(
                f"Fail send message: '{ret.url}'", ret.status, ret.data
            )

    def send_multiple(
        self, data_input: List[GroupLogElement], uuid_group: Optional[int] = None
    ) -> None:
        """Send multiple log message to the server.
        :param data: Data to send to the server
        :param uuid_group: local internal group UUID
        """
        data = []
        for elem in data_input:
            if elem.time is not None:
                data.append(
                    {
                        "id": elem.id,
                        "time": elem.time.astimezone(timezone.utc).isoformat(),
                        "data": elem.data,
                    }
                )
            else:
                data.append(
                    {
                        "id": elem.id,
                        "time": datetime.now().astimezone(timezone.utc).isoformat(),
                        "data": elem.data,
                    }
                )


        param = {}
        if uuid_group is not None:
            param["uuid"] = uuid_group
        ret = self.connection.post(
            self.service, f"{self.system}/push_multiple", data=data, params=param
        )
        if ret is None:
            raise KaranageException(
                f"Fail send message sub-library return None")
        if ret.status is None or not 200 <= ret.status <= 299:
            raise KaranageException(
                f"Fail send message: '{ret.url}'", ret.status, ret.data
            )
