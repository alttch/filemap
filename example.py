from filemap import FileMap

m = FileMap() #'example')

m.update('example', raw=False)

print(m.get('somekey1'))
print(m.get('some.another.key'))

print(m.data.somekey1)
print(m.data.some.another.key)

from pprint import pprint
pprint(FileMap('example', raw=False).serialize())
