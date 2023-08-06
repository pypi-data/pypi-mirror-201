#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   __init__.pyi
# @Created At:  2022-08-03 09:47:47
# @Modified At: 2023-04-07 13:58:38
# @Modified By: thepoy

from .tfidf import TFIDF
from .textrank import TextRank

default_tfidf: TFIDF
default_textrank: TextRank

extract_tags = tfidf = default_tfidf.extract_tags
set_idf_path = default_tfidf.set_idf_path
textrank = default_textrank.extract_tags

def set_stop_words(stop_words_path: str) -> None: ...
