# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-11 23:25:36
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's regular methods.
"""


from typing import List, Tuple, Optional, Union, Literal, overload
import re
from re import RegexFlag


def re_search(pattern: str, text: str, mode: Optional[RegexFlag] = None) -> Optional[Union[str, Tuple[Optional[str], ...]]]:
    """
    Regular matching text.

    Parameters
    ----------
    pattern : Regular pattern.
    text : Match text.
    mode : Regular mode.
        - None : No mode.
        - RegexFlag : Use this mode, ojbect from package re.

    Returns
    -------
    Matching result.
        - When match to and not use group, then return string.
        - When match to and use group, then return tuple with value string or None.
        - When no match, then return.
    """

    # Search.
    if mode == None:
        obj_re = re.search(pattern, text)
    else:
        obj_re = re.search(pattern, text, mode)

    # Return result.
    if obj_re != None:
        result = obj_re.groups()
        if result == ():
            result = obj_re[0]
        return result

@overload
def res(text: str, *patterns: str, return_first: bool = True) -> Union[
    Optional[Union[str, Tuple[Optional[str], ...]]],
    List[Optional[Union[str, Tuple[Optional[str], ...]]]]
]: ...

@overload
def res(return_first: Literal[True]) -> Optional[Union[str, Tuple[Optional[str], ...]]]: ...

@overload
def res(return_first: Literal[False]) -> List[Optional[Union[str, Tuple[Optional[str], ...]]]]: ...

def res(text: str, *patterns: str, return_first: bool = True) -> Union[
    Optional[Union[str, Tuple[Optional[str], ...]]],
    List[Optional[Union[str, Tuple[Optional[str], ...]]]]
]:
    """
    Batch regular matching text.

    Parameters
    ----------
    text : Match text.
    pattern : Regular pattern.
    return_first : Whether return first successful match.

    Returns
    -------
    Matching result.
        - When match to and not use group, then return string.
        - When match to and use group, then return tuple with value string or None.
        - When no match, then return.
    """

    # Search.

    ## Return first result.
    if return_first:
        for pattern in patterns:
            result = re_search(pattern, text)
            if result != None:
                return result

    ## Return all result.
    else:
        result = [re_search(pattern, text) for pattern in patterns]
        return result