# -*- coding: utf-8 -*-
"""worldcat's parser: convert database exports into semi-structured format."""
from .worldcat import Parser, load, loads, save

__all__ = ["Parser", "load", "loads", "save"]
