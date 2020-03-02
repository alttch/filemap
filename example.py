from filemap import FileMap

m = FileMap()  #'example')

m.update('example', types={'somejkey': 'json', 'somekey2': float, 'someboolkey': bool, 'somebinkey': 'raw'})

print(m.get('somekey1'))
print(m.get('some.another.key'))

print(m.data.somekey1)
print(m.data.somekey2 + 100)
print(m.data.some.another.key)
print(m.data.somejkey['a'])

# TODO: move this to pytest
assert m.get('somekey4', 5) == 5
assert m.get('somekey4', None) is None
try:
    assert m.get('somekey4') is None
    raise RuntimeError('key error not raised')
except AttributeError:
    pass

from pprint import pprint
pprint(dict(m))
print()
print()
pprint(FileMap('example', default_type='raw').serialize())
