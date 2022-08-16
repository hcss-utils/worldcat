import pytest
import worldcat


@pytest.fixture
def parser():
    return worldcat.Parser()
