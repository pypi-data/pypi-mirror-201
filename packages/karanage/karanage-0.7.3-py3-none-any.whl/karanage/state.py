#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
import enum
import json
from typing import Any, Dict, Optional, Union, List, NamedTuple

from datetime import datetime, timezone
import requests

from .connection import KaranageConnectionInterface
from .exception import KaranageException


class StateSystem(enum.Enum):
    OK = "OK"
    FAIL = "FAIL"
    DOWN = "DOWN"

class StateData(NamedTuple):
    topic: str
    time: datetime
    state: str
    data: Dict

def convert_to_state_data(json_data: Dict, topic:Optional[str] = None) -> StateData:
    time = datetime.fromtimestamp(json_data["time"], timezone.utc)
    if topic is not None:
        topic = topic
    else:
        topic = json_data["topic"]
    return StateData(topic, time, json_data["state"], json_data["data"])



## Generic karanage sending system.
class KaranageState:
    def __init__(self, connection: KaranageConnectionInterface) -> None:
        """Initialize the communication class.
        :param connection: Connection interface.
        """
        self.connection = connection

    def send(
        self,
        topic: str,
        data: Optional[Dict] = None,
        state: StateSystem = StateSystem.OK,
    ) -> None:
        """Send a message to the server.
        :param topic: Topic where to publish the data.
        :param data: Data to send to the server
        :param state: State of the current system
        """
        if data is None:
            data = {}
        param = {}
        if state is not None:
            param["state"] = state.value
        ret = self.connection.post("state", topic, data=data, params=param)
        if ret is None:
            raise KaranageException(
                f"Fail send message sub-library return None")
        if ret.status is None or not 200 <= ret.status <= 299:
            raise KaranageException(
                f"Fail send message: '{ret.url}'", ret.status, ret.data
            )

    def get(self, topic: str, since: Union[None, str, datetime] = None) -> Optional[StateData]:
        """Get all the topic fom the server.
        :param since: ISO1866 time value.
        :return: A dictionary with the requested data.
        """
        param = {
            "mode":"raw" # request raw mode to have the timestamp in a float in second
        }
        if since is not None:
            if type(since) is str:
                param["since"] = since
            elif type(since) is datetime:
                param["since"] = since.replace(tzinfo=timezone.utc).isoformat()
            else:
                raise KaranageException(
                    f"Wrong input parameter type Must be a str or datetime: '{type(since)}'")
        ret = self.connection.get("state", topic, params=param)
        if ret is None:
            raise KaranageException(
                f"Fail send message sub-library return None")
        if ret.status is not None and 200 <= ret.status <= 299:
            if ret.data == "":
                return None
            return convert_to_state_data(json.loads(ret.data), topic)
        return None
        #raise KaranageException(f"Fail get data: '{ret.url}'", ret.status, ret.data)

    def gets(self, since: Union[None, str, datetime] = None) -> List[StateData]:
        """Get all the topic fom the server.
        :param since: ISO1866 time value.
        :return: A dictionary with the requested data.
        """
        param = {
            "mode":"raw" # request raw mode to have the timestamp in a float in second
        }
        if since is not None:
            if type(since) is str:
                param["since"] = since
            elif type(since) is datetime:
                param["since"] = since.replace(tzinfo=timezone.utc).isoformat()
            else:
                raise KaranageException(
                    f"Wrong input parameter type Must be a str or datetime: '{type(since)}'")
        ret = self.connection.get("state", params=param)
        if ret is None:
            raise KaranageException(
                f"Fail send message sub-library return None")
        if ret.status is not None and 200 <= ret.status <= 299:
            out: List[StateData] = []
            if ret.data is not None:
                for elem in json.loads(ret.data):
                    out.append(convert_to_state_data(elem))
            return out
        raise KaranageException(f"Fail get data: '{ret.url}'", ret.status, ret.data)

    def get_history(
        self,
        topic: Optional[str] = None,
        since: Union[None, str, datetime] = None,
        since_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[StateData]:
        """Get all the topic fom the server.
        :param since: ISO1866 time value.
        :param since_id: remote BDD index of the field.
        :param limit: the number of value we want to get
        :return: A dictionary with the requested data.
        """
        param:Dict[str, Any] = {

            "mode":"raw" # request raw mode to have the timestant in a float in second
        }
        if since is not None:
            if type(since) is str:
                param["since"] = since
            elif type(since) is datetime:
                param["since"] = since.replace(tzinfo=timezone.utc).isoformat()
            else:
                raise KaranageException(
                    f"Wrong input parameter type Must be a str or datetime: '{type(since)}' {type(str)}")
        if since_id is not None:
            param["sinceId"] = since_id
        if limit is not None:
            param["limit"] = limit
        ret = self.connection.get("state_history", topic, params=param)
        if ret is None:
            raise KaranageException(
                f"Fail send message sub-library return None")
        if ret.status is not None and 200 <= ret.status <= 299:
            out: List[StateData] = []
            if ret.data is not None:
                for elem in json.loads(ret.data):
                    out.append(convert_to_state_data(elem, topic))
            return out
        raise KaranageException(f"Fail get data: '{ret.url}'", ret.status, ret.data)
