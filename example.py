from filemap import FileMap

m = FileMap('example')

print(m.get('somekey1'))
print(m.get('some.another.key'))

print(m.data.somekey1)
print(m.data.some.another.key)

from pprint import pprint
pprint(FileMap('example').serialize())
