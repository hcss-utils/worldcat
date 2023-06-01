# -*- coding: utf-8 -*-
import pytest

import worldcat


@pytest.mark.parametrize(
    "mapping,expected_mapping,list_tags,expected_list_tags",
    [
        (None, 33, ["a"], 1),
        (["a", "b"], 2, None, 4),
        (["z", "x", "c"], 3, ["z", "x", "c"], 3),
    ],
)
def test_new_parser(mapping, expected_mapping, list_tags, expected_list_tags):
    parser = worldcat.Parser(mapping=mapping, list_tags=list_tags)
    assert len(parser.mapping) == expected_mapping
    assert len(parser.list_tags) == expected_list_tags


def test_loads(document):
    data = worldcat.loads(document)
    assert len(data) == 1
    parsed_document = data[0]
    assert isinstance(parsed_document, dict)
    assert parsed_document["Title"] == (
        "Gazprom: russia's nationalized political weapon "
        "and the implications for the european union"
    )
    assert parsed_document["Year"] == "2012"
    assert parsed_document["Identifier"] == "European Union, Gazprom, Kremlin, Russia"
    assert len(parsed_document["Descriptor"]) == 4
    assert parsed_document["Publication"] == "Washington, DC Georgetown University"


def test_load(tmp_path, document):
    # replacing pathlib's read_txt with a lambda function
    # as I don't want to read from file while testing
    filepath = tmp_path / "document.txt"
    filepath.write_text(document)
    data = worldcat.load(filepath, encoding="utf-8")
    assert len(data) == 1
    parsed_document = data[0]
    assert isinstance(parsed_document, dict)
    assert parsed_document["Title"] == (
        "Gazprom: russia's nationalized political weapon "
        "and the implications for the european union"
    )
    assert parsed_document["Year"] == "2012"
    assert parsed_document["Identifier"] == "European Union, Gazprom, Kremlin, Russia"
    assert len(parsed_document["Descriptor"]) == 4
    assert parsed_document["Publication"] == "Washington, DC Georgetown University"


def test_save(document, tmp_path):
    output_file = tmp_path / "parsed.json"
    assert not output_file.exists()
    data = worldcat.loads(document)
    worldcat.save(data, output_file)
    assert output_file.exists()


def test_parse(document):
    parser = worldcat.Parser()
    data = parser.parse(document)
    assert len(data) == 1
    parsed_document = data[0]
    assert isinstance(parsed_document, dict)
    assert parsed_document["Title"] == (
        "Gazprom: russia's nationalized political weapon "
        "and the implications for the european union"
    )
    assert parsed_document["Year"] == "2012"
    assert parsed_document["Identifier"] == "European Union, Gazprom, Kremlin, Russia"
    assert len(parsed_document["Descriptor"]) == 4
    assert parsed_document["Publication"] == "Washington, DC Georgetown University"
