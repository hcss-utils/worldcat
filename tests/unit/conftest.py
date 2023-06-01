# -*- coding: utf-8 -*-
import pytest

import worldcat


@pytest.fixture
def parser():
    return worldcat.Parser()
