import re
import pytest


def test_parse_failure(parser):
    with pytest.raises(TypeError):
        parser.parse(None)


@pytest.mark.parametrize(
    "corpus,expected_result",
    [
        ("Title: oops".join("-" * 200 for _ in range(5)), 4),
        ("irrelevant: fields\n".join("-" * 200 for _ in range(5)), 0),
        ("separated", 0),
    ],
)
def test__split_corpus(parser, corpus, expected_result):
    response = parser.parse(corpus)
    assert isinstance(response, list)
    assert len(response) == expected_result


def test__parse_document(parser, document):
    response = parser._parse_document(document)
    # parsed but not yet flattened
    assert response["Publication"] == ["Washington, DC Georgetown University"]
    assert response["Year"] == ["2012"]


def test__parse_line(parser, document):
    lines = document.split("\n")
    sample_line1 = lines[21]
    sample_line2 = lines[7]
    sample_line3 = lines[50]

    # parsed as tuples with multiple whitespaces
    tup1 = parser._parse_line(sample_line1)
    assert tup1 == ("Find Items About", "         Georgetown University,2,296")
    optional_tup = parser._parse_line(sample_line2)
    assert optional_tup is None
    tup2 = parser._parse_line(sample_line3)
    assert tup2 == ("Descriptor", "               International relations.")


def test__parse_named_field(parser, document):
    lines = document.split("\n")
    sample_line = lines[2]
    response = parser._parse_named_field(sample_line)
    assert response is None


def test__parse_anon_field(parser, document):
    lines = document.split("\n")
    first_line = lines[0]
    response = parser._parse_anon_field(first_line)
    assert response is None


def test__preprocess(parser):
    processed = parser._preprocess("               International relations.")
    assert processed == "International relations."


def test__flatten_fields(parser, document):
    response = parser._parse_document(document)
    flattened_response = parser._flatten_fields(response)
    assert flattened_response["Publication"] == "Washington, DC Georgetown University"
    assert flattened_response["Year"] == "2012"
