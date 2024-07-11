import fnmatch
import os
import re
from typing import List

from source.common.domain.string_engine.base_file_search import StringSearchAlgorithm
from source.common.schema.core_schema import FilePath


def find_files_with_substrings(directory: FilePath, substring: str):
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatchcase(filename.lower(), f'*{substring.lower()}*'):
                matches.append(os.path.join(root, filename))
    return matches


class SimpleSubstringStringMatcher(StringSearchAlgorithm):
    def __call__(self, key: str):
        return find_files_with_substrings(self.directory, substring=key)


def find_files_with_regex(directory: str, pattern: str) -> List[str]:
    regex = re.compile(pattern, re.IGNORECASE)
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if regex.search(filename):
                matches.append(os.path.join(root, filename))
    return matches


class RegexStringMatcher(StringSearchAlgorithm):
    def __call__(self, key: str):
        return find_files_with_regex(self.directory, pattern=key)


def find_files_with_exact_match(directory: str, exact_name: str) -> List[str]:
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower() == exact_name.lower():
                matches.append(os.path.join(root, filename))
    return matches


class ExactStringMatcher(StringSearchAlgorithm):
    def __call__(self, key: str):
        return find_files_with_exact_match(self.directory, exact_name=key)


def find_files_with_prefix(directory: str, prefix: str) -> List[str]:
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().startswith(prefix.lower()):
                matches.append(os.path.join(root, filename))
    return matches


class PrefixStringMatcher(StringSearchAlgorithm):
    def __call__(self, key: str):
        return find_files_with_prefix(self.directory, prefix=key)


def find_files_with_suffix(directory: str, suffix: str) -> List[str]:
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(suffix.lower()):
                matches.append(os.path.join(root, filename))
    return matches


class SuffixStringMatcher(StringSearchAlgorithm):
    def __call__(self, key: str):
        return find_files_with_suffix(self.directory, suffix=key)
