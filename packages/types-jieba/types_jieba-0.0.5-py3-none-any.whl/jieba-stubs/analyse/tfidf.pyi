#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   tfidf.pyi
# @Created At:  2022-08-03 09:47:47
# @Modified At: 2023-04-07 14:00:34
# @Modified By: thepoy

from typing import Dict, List, Set, Tuple, Any
from abc import abstractmethod
from jieba import Tokenizer
from jieba.posseg import POSTokenizer

DEFAULT_IDF: str

class KeywordExtractor:
    STOP_WORDS: Set[str]

    def set_stop_words(self, stop_words_path: str) -> None: ...
    @abstractmethod
    def extract_tags(self, *args: Any, **kwargs: Dict[str, Any]) -> None: ...

class IDFLoader(object):
    path: str
    idf_freq: Dict[str, float]
    median_idf: float

    def __init__(self, idf_path: str | None = ...) -> None: ...
    def set_new_path(self, new_idf_path: str) -> None: ...
    def get_idf(self) -> Tuple[Dict[str, float], float]: ...

class TFIDF(KeywordExtractor):
    tokenizer: Tokenizer
    postokenizer: POSTokenizer
    stop_words: Set[str]
    idf_loader: IDFLoader
    idf_freq: Dict[str, float]
    median_idf: float

    def __init__(self, idf_path: str | None = ...) -> None: ...
    def set_idf_path(self, idf_path: str) -> None: ...
    def extract_tags(
        self,
        sentence: str,
        topK: int = ...,
        withWeight: bool = ...,
        allowPOS: Tuple[str, ...] = ...,
        withFlag: bool = ...,
    ) -> List[Tuple[str, float] | str]: ...
