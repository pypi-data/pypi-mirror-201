# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-08 11:07:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's request methods.
"""


from typing import List, Dict, Tuple, Literal, Optional, Union
import requests
from requests import Response, JSONDecodeError
from faker import Faker

from .rbasic import get_first_notnull
from . import roption


# Global variable Faker object.
fake: Faker = Faker("zh_CN")

def fake_headers() -> Dict:
    """
    Fake request headers.

    Returns
    -------
    Fake request headers.
    """

    # Generate.
    headers = {}
    headers['user_agent'] = fake.android_platform_token()

    return headers

def check_response(
        response: Response,
        code_fields: Optional[List] = None,
        success_codes: Optional[List] = None,
        throw_error: bool = True
    ) -> Tuple[int, str]:
    """
    Check whether reponse is successful

    Parameters
    ----------
    response : Object from requests package.
    code_fields : Possible field names of Response code in Response data.
        - None : Use option of module roption.
        - List : Use this value.

    success_codes : Successful codes.
        - None : Use option of module roption.
        - List : Use this value.

    throw_error : Whether throw error.

    Returns
    -------
    Response code and Response message
    """

    # Get parameters by priority.
    code_fields = get_first_notnull(code_fields, roption.code_fields)
    success_codes = get_first_notnull(success_codes, roption.success_codes)

    # Check.

    ## Check request code.
    reponse_code = response.status_code
    if reponse_code not in success_codes:
        check_info = reponse_code, response.text
        if throw_error:
            raise AssertionError(reponse_code, response.text)
        return check_info

    ## Check route code.
    try:
        response_data = response.json()
    except JSONDecodeError:
        return 200, "success"
    if type(response_data) == dict:
        for field in code_fields:
            if field in response_data:
                code = response_data[field]
                if code in success_codes:
                    break
                else:
                    check_info = code, response_data
                    if throw_error:
                        raise AssertionError(code, response_data)
                    return check_info

    return 200, "success"

def request(
    url: str,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None,
    headers: Optional[Union[Dict, Literal["fake"]]] = None,
    timeout: Optional[Union[int, float]] = None,
    proxies: Optional[Dict[str, str]] = None,
    method: Optional[Literal["get", "post"]] = None,
    check: bool = False,
    code_fields: Optional[List] = None,
    success_codes: Optional[List] = None
    ) -> Response:
    """
    Send HTTP request.

    Parameters
    ----------
    url : Request URL.
    data : Request data. Parameter data and json conflict.
    json : Request data in JSON format. Parameter data and json conflict.
    headers : Request header.
        - None : No request header.
        - Dict : Use dict as request header.
        - Literal['fake'] : Use fake request header.

    timeout : Request maximun waiting time.
        - None : No limit.
        - int, float : Use this value.
    
    proxies : IP proxy setup.
        - None : No setup.
        - Dict[str, str] : Name and use IP of each protocol.

    method : Request method.
        - None : Automatic judge.
            * When parameter data or json not has value, then request method is get.
            * When parameter data or json has value, then request method is post.
        - Literal['get'] : Request method is get.
        - Literal['post'] : Request method is post.

    check : Whether check response.
    code_fields : Possible field names of Response code in Response data.
        - None : Use option of module roption.
        - List : Use this value.

    success_codes : Successful codes.
        - None : Use option of module roption.
        - List : Use this value.

    Returns
    -------
    Response object of requests package.
    """

    # Get parameters by priority.
    code_fields = get_first_notnull(code_fields, roption.code_fields)
    success_codes = get_first_notnull(success_codes, roption.success_codes)

    # Handle parameters.
    if method == None:
        if data == None and json == None:
            method = "get"
        else:
            method = "post"
    if headers == "fake":
        headers = fake_headers()

    # Request.
    if method == "get":
        response = requests.get(url, data=data, json=json, headers=headers, timeout=timeout, proxies=proxies)
    elif method == "post":
        response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout, proxies=proxies)

    # Check.
    if check:
        check_response(response, code_fields, success_codes)

    return response