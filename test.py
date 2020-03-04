#!/usr/bin/env pytest

import pytest
from filemap import FileMap

m = FileMap()  #'example')


def test_update():
    m.update('test_data',
             types={
                 'somejkey': 'json',
                 'somekey2': float,
                 'someboolkey': bool,
                 'somebinkey': 'raw'
             })


def test_get():
    assert m.get('somekey1') == 'value1'
    assert m.get('some.another.key') == 'value3'
    assert m.data.somekey1 == 'value1'
    assert m.data.somekey2 == 34.55
    assert m.data.some.another.key == 'value3'
    assert m.data.somebinkey == b'xxx\n'
    assert m.data.somejkey['a'][1] == 2
    assert m.get('somekey4', 5) == 5
    assert m.get('somekey4', None) is None
    assert m.get('someboolkey') is True
    assert dict(m)['somekey1'] == 'value1'
    with pytest.raises(AttributeError):
        assert m.get('somekey4') is None


def test_raw():
    assert FileMap('test_data',
                   default_type='raw').get('somekey1') == b'value1\n'
