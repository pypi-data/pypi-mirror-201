#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   viterbi.pyi
# @Created At:  2022-08-03 09:47:47
# @Modified At: 2023-04-07 13:58:22
# @Modified By: thepoy

from typing import List, Tuple
from . import StatesType, StartType, TransType, EmitType

MIN_FLOAT: float
MIN_INF: float

def viterbi(
    obs: str,
    states: StatesType,
    start_p: StartType,
    trans_p: TransType,
    emit_p: EmitType,
) -> Tuple[str, List[Tuple[str, str]]]: ...
