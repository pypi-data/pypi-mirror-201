import copy
import json
import logging
import time
import uuid
from json import JSONDecodeError

import deepdiff
import redis
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


class JWTSetup:
    """
    Class for storing redis config data
    """
    r = None
    channel = None
    pub = None
    res = None

    @staticmethod
    def init(r, channel, pub, res):
        """
        Apply config
        :param r: redis instance
        :type r: redis
        :param channel: redis channel name
        :type channel: str
        :param pub: publish message template
        :type pub: str
        :param res: response message template
        :type res: str
        """
        JWTSetup.r = r
        JWTSetup.channel = channel
        JWTSetup.pub = pub
        JWTSetup.res = res


async def jwt_redis_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    if not JWTSetup.pub or not JWTSetup.res or not JWTSetup.channel or not JWTSetup.r:
        raise redis.exceptions.ConnectionError
    publish_message = copy.deepcopy(JWTSetup.pub)
    response_message = copy.deepcopy(JWTSetup.res)

    logging.info("Authorization")
    token = credentials.credentials

    request_id = str(uuid.uuid4())

    try:
        logging.info("Connecting to Redis Server")
        redis_client = JWTSetup.r.client()
        pubsub = redis_client.pubsub()
        pubsub.subscribe(JWTSetup.channel + ".reply")

        publish_message = _transform_dict(publish_message, token, request_id)
        response_message = _transform_dict(response_message, "", request_id)

        logging.info(
            "Publishing message to Redis server for token validation.")
        redis_client.publish(
            JWTSetup.channel,
            json.dumps(publish_message),
        )

        try:
            timeout = 5.0
            live_timeout = time.time() + 5
            logging.info("Waiting for Redis response.")
            while True:
                if time.time() > live_timeout:
                    raise TimeoutError
                message = pubsub.get_message(timeout=timeout)
                if message and message["type"] == "message":
                    redis_response = {}
                    for key, value in message.items():
                        redis_response[key] = _transform_redis_response(value)
                    diff = deepdiff.DeepDiff(response_message, redis_response)
                    if diff == {}:
                        logging.info("Redis response - Token is valid")
                        break
                    if "type_changes" in diff:
                        logging.info(
                            "Redis response - Token is invalid")
                        redis_client.close()
                        raise HTTPException(
                            status_code=401,
                            detail=f"Unauthorized",
                        )
                    values = diff.get("values_changed", {})
                    for change in values.values():
                        if change["old_value"] != request_id:
                            logging.info("Redis response - Token is invalid")
                            redis_client.close()
                            raise HTTPException(
                                status_code=401,
                                detail="Unauthorized")
        except TimeoutError:
            logging.error(
                "Haven't received any answer from Redis for 5 seconds."
            )
            redis_client.close()
            raise HTTPException(
                status_code=504,
                detail="Gateway Timeout")
        redis_client.close()
    except redis.exceptions.ConnectionError:
        logging.error("Redis refused to connect.")
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway")


def _transform_dict(data, new_token: str = "", new_id: str = "") -> dict:
    """
    Function to insert into given dictionary `Token` and `ID` fields.
    returns and
    :param data: Dictionary where to apply transformation
    :type data: dict
    :param new_token: Token string to place in dictionary
    :type new_token: str
    :param new_id: ID string to place in dictionary
    :type new_id: str
    :return: Transformed dictionary
    :rtype: dict
    """
    working_dict = copy.deepcopy(data)
    for key, value in working_dict.items():
        if working_dict[key] == "TOKEN":
            working_dict[key] = new_token
        elif working_dict[key] == "ID":
            working_dict[key] = new_id
        elif isinstance(value, dict):
            working_dict[key] = _transform_dict(value, new_token, new_id)
    return working_dict


def _transform_redis_response(data):
    """
    Function to transform response from Redis message broker to Python Dictionary
    :param data: Redis response values
    :type data: all
    :return: Returns transformed redis value
    :rtype: all
    """
    try:
        if isinstance(data, dict):
            loaded_d = data
        else:
            loaded_d = json.loads(data)
        for key, value in loaded_d.items():
            loaded_d[key] = _transform_redis_response(value)
    except (JSONDecodeError, TypeError):
        if isinstance(data, bytes):
            return data.decode("utf-8")
        return data
    return loaded_d
