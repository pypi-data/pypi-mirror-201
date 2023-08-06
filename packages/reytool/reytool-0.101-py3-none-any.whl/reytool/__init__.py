# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:21
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's personal tool set.
"""


from typing import Final

from .rbasic import warn
from .rcompress import rzip
from .rcommon import exc, digits, randn, sleep, get_paths, n_to_ch
from .rdata import count, flatten, split, distinct
from .rdatabase import REngine, RConnection
from .rdatetime import RDateTimeMark, now
from .remail import REmail
from .rmultitask import threads
from . import roption
from .rregular import res
from .rrequest import request
from .rtext import rprint
from .rwrap import runtime


__version__: Final[str] = "0.101"