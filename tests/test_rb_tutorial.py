# -*- coding: utf-8 -*-
import pytest


@pytest.mark.unit
@pytest.mark.parametrize("key, expected_value", [
    ("__name__", "rb_tutorial"),
    ("__description__", "Rogue Basin's Complete Python 3 Tutorial"),
    ("__author__", "Brian Bruggeman"),
    ("__author_email__", "brian.m.bruggeman@gmail.com"),
    ("__maintainer__", "Brian Bruggeman"),
    ("__maintainer_email__", "brian.m.bruggeman@gmail.com"),
    ("__url__", "http://www.pypi.org"),
    ("__version__", "0.1.0"),
    ("__version_info__", (0, 1, 0)),
])
def test_project_metadata(key, expected_value):
    import rb_tutorial

    fields = [_ for _ in dir(rb_tutorial)]
    value = getattr(rb_tutorial, key, None)
    assert key in fields
    assert value == expected_value


@pytest.mark.unit
@pytest.mark.parametrize("exc_name", [
    'BaseException'
])
def test_project_exceptions(exc_name):
    from rb_tutorial import exceptions

    assert hasattr(exceptions, exc_name)
    Exception = getattr(exceptions, exc_name)
    with pytest.raises(Exception):
        raise Exception()
