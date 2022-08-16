import collections
import re
import typing
from pathlib import Path

from worldcat.config import DEFAULT_FIELDNAMES

JSON = typing.Dict[str, typing.Any]


class Parser:

    DOCUMENT_SEPARATOR = "-" * 200
    NEWLINE = "\n"
    NAMED_FIELD_PATTERN = r"^[^:]+:\s"
    NAMED_FIELD_SEPARATOR = ":"
    FIELDNAMES = DEFAULT_FIELDNAMES

    def __init__(self, *, mapping: typing.Optional[typing.Dict[str, str]] = None):
        self.mapping = self.FIELDNAMES if mapping is None else mapping

    def parse(self, text: str) -> typing.List[JSON]:
        data = []
        documents = self._split_coprus(text)
        for document in documents:
            parsed_document = self._parse_document(document)
            data.append(parsed_document)
        return data

    def _split_coprus(self, text: str) -> typing.List[str]:
        return re.split(self.DOCUMENT_SEPARATOR, text)

    def _parse_document(self, document: str) -> JSON:
        self.last_tag = None
        data = collections.defaultdict(list)
        for line in re.split(self.NEWLINE, document):
            if line.endswith(":"):
                line = f"{line} "
            parsed_line = self._parse_line(line)
            if parsed_line is None:
                continue
            key, value = parsed_line
            data[key].append(value)
        return data

    def _parse_line(self, line: str) -> typing.Optional[typing.Tuple[str, typing.Any]]:
        if re.match(self.NAMED_FIELD_PATTERN, line):
            return self._parse_named_field(line)
        return self._parse_anon_field(line)

    def _parse_named_field(
        self, line: str
    ) -> typing.Optional[typing.Tuple[str, typing.Any]]:
        key, value = line.split(self.NAMED_FIELD_SEPARATOR, maxsplit=1)
        field_name = key.strip()
        if field_name in self.mapping:
            self.last_tag = field_name
            return field_name, value
        return None

    def _parse_anon_field(
        self, line: str
    ) -> typing.Optional[typing.Tuple[str, typing.Any]]:
        if line == "":
            return None
        if self.last_tag is not None:
            return self.last_tag, line
        return None


def load(
    file: Path,
    *,
    encoding: typing.Optional[str] = None,
    implementation: typing.Optional[Parser] = None,
    **kwargs,
) -> typing.List[JSON]:
    text = file.read_text(encoding=encoding)
    return loads(text, implementation=implementation, **kwargs)


def loads(
    text: str, *, implementation: typing.Optional[Parser] = None, **kwargs
) -> typing.List[JSON]:
    parser = Parser(**kwargs) if implementation is None else implementation
    return parser.parse(text)
