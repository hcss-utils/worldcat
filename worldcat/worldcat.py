# -*- coding: utf-8 -*-
"""This module contains worldcat's export Parser."""
import collections
import json
import re
import typing
from pathlib import Path

from .config import DEFAULT_FIELDNAMES, DEFAULT_LIST_TAGS

JSON = typing.Dict[str, typing.Any]
ParsedField = typing.Tuple[str, typing.Any]


class Parser:
    """Worldcat's export parser."""

    DOCUMENT_SEPARATOR = "-" * 200
    NEWLINE = "\n"
    NAMED_FIELD_PATTERN = r"^[^:]+:\s"
    NAMED_FIELD_SEPARATOR = ":"
    FIELDNAMES = DEFAULT_FIELDNAMES
    FIELDNAMES_LIST = DEFAULT_LIST_TAGS

    def __init__(
        self,
        *,
        mapping: typing.Optional[typing.List[str]] = None,
        list_tags: typing.Optional[typing.List[str]] = None,
    ):
        self.mapping = self.FIELDNAMES if mapping is None else mapping
        self.list_tags = self.FIELDNAMES_LIST if list_tags is None else list_tags
        self.last_tag: typing.Optional[str] = None

    def parse(self, text: str) -> typing.List[JSON]:
        """Parses .txt export into semi-structure format."""
        data = []
        documents = self._split_coprus(text)
        for document in documents:
            parsed_document = self._parse_document(document)
            if len(parsed_document) != 0:
                data.append(self._flatten_fields(parsed_document))
        return data

    def _split_coprus(self, text: str) -> typing.List[str]:
        """Splits corpus -- a collection of documents stored in one .txt file,
        as a text delimited with special chars -- into a list of documents."""
        return re.split(self.DOCUMENT_SEPARATOR, text)

    def _parse_document(self, document: str) -> JSON:
        """Parses a single document."""
        self.last_tag = None
        data = collections.defaultdict(list)
        for line in re.split(self.NEWLINE, document):
            if line.endswith(":"):
                line += " "
            parsed_line = self._parse_line(line)
            if parsed_line is None:
                continue
            key, value = parsed_line
            data[key].append(self._preprocess(value))
        return data

    def _parse_line(self, line: str) -> typing.Optional[ParsedField]:
        """Parses a single line."""
        if re.match(self.NAMED_FIELD_PATTERN, line):
            return self._parse_named_field(line)
        return self._parse_anon_field(line)

    def _parse_named_field(self, line: str) -> typing.Optional[ParsedField]:
        """Parses a single line that matches named field pattern."""
        key, value = line.split(self.NAMED_FIELD_SEPARATOR, maxsplit=1)
        field_name = key.strip()
        if field_name in self.mapping:
            self.last_tag = field_name
            return field_name, value
        return None

    def _parse_anon_field(self, line: str) -> typing.Optional[ParsedField]:
        """Parses a single line that does not match a named field pattern."""
        if line == "":
            return None
        if self.last_tag is not None:
            return self.last_tag, line
        return None

    def _preprocess(self, text: str) -> str:
        """Preprocesses input text.

        !todo: update preprocessing with additional steps
        """
        return re.sub(r"\s+", " ", text).strip()

    def _flatten_fields(self, data: JSON, sep: str = " ") -> JSON:
        """Flattens dict's values.

        Notes
        -----
        Since worldcat's format contains multiline fields, we use defaultdict
        by default, so that whenever we have multiline fields, we extend data
        instead of replacing 'old' entries with the 'new' ones.
        Then, depending on config, we flatten most of the fields.
        """
        data_copy = data.copy()
        for field_name, nested_values in data_copy.items():
            if field_name in self.list_tags:
                continue
            data_copy[field_name] = sep.join(set(nested_values))
        return data_copy


def load(
    file: Path,
    *,
    encoding: typing.Optional[str] = None,
    implementation: typing.Optional[Parser] = None,
    **kwargs: typing.Any,
) -> typing.List[JSON]:
    """Loads a .txt file with exported documents and returns
    processed documents in semi-structured format."""
    text = file.read_text(encoding=encoding)
    return loads(text, implementation=implementation, **kwargs)


def loads(
    text: str, *, implementation: typing.Optional[Parser] = None, **kwargs: typing.Any
) -> typing.List[JSON]:
    """Loads a string of documents and returns a processed documents
    in semi-structured format."""
    parser = Parser(**kwargs) if implementation is None else implementation
    return parser.parse(text)


def save(
    data: typing.Union[JSON, typing.List[JSON]],
    file: Path,
    *,
    encoding: str = "utf-8",
    **kwargs: typing.Any,
) -> None:
    """Saves processed documents to .json file."""
    with file.open("w", encoding=encoding) as output_file:
        json.dump(data, output_file, **kwargs)
