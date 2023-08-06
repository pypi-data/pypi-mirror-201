# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-02-18 19:27:04
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's method options.
"""


from typing import List, Literal


# Default width of method rprint.
print_width: int = 100

# Default frame type of method rprint.
print_default_frame_full: Literal["full", "half", "plain"] = "full"
print_default_frame_half: Literal["full", "half", "plain"] = "half"

# Possible field names of Response code in Response data of method request.
code_fields: List = ["code", "errno", "success"]

# Successful codes of method request.
success_codes: List = [200, 204, 0, True]
success_codes.extend(
    [
        str(code)
        for code in success_codes
        if type(code) == int
    ]
)