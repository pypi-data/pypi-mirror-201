#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   textrank.pyi
# @Created At:  2022-08-03 09:47:47
# @Modified At: 2023-04-07 14:00:55
# @Modified By: thepoy

from collections import defaultdict
from jieba import Tokenizer
from jieba.posseg import pair
from .tfidf import KeywordExtractor
from typing import List, Set, Tuple

class UndirectWeightedGraph:
    d: float
    graph: defaultdict[float, List[Tuple[float, float, float]]]

    def addEdge(self, start: float, end: float, weight: float) -> None: ...
    def rank(self) -> defaultdict[float, float]: ...

class TextRank(KeywordExtractor):
    tokenizer: Tokenizer
    postokenizer = tokenizer
    stop_words: Set[str]
    pos_filt: frozenset[str]
    span: int

    def pairfilter(self, wp: pair) -> bool: ...
    def textrank(
        self,
        sentence: str,
        topK: int = ...,
        withWeight: bool = ...,
        allowPOS: Tuple[str, ...] = ...,
        withFlag: bool = ...,
    ) -> List[Tuple[str, float] | str]: ...
