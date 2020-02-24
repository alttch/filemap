# filemap - processing Kubernetes-style config maps and secrets

## What's this

**filemap** is a Python module for comfortable processing of Kubernetes-style
config maps and secrets, mounted as the volumes.

## Usage

When connected as volumes, Kubernetes config maps and secrets are single-level
directory, where files are keys and file contents are values.

### Basic usage

When loaded, inside **FileMap** object, keys are transformed into fields and
namespaces, field trees are formed with the dots in file names, as:

* somefile => obj.data.somefile
* some.key => obj.data.some.key
* some.another.key => obj.data.some.another.key

Example:

```python
from filemap import FileMap

config = FileMap('/etc/config')

print(config.data.somefile)
print(config.data.some.key)
print(config.data.some.another.key)
```

Note: when text data is loaded, it's automatically right-stripped.

### Getting single key by name

```python
print(config.get('some.key'))
print(config.get('some.another.key'))
```

### Serialization to dict

When serialized, **FileMap** object is transformed into dict:

```python
data = config.serialize()
print(data['somefile'])
print(data['some']['file'])
print(data['some']['another']['file'])
```

### Combining multiple volumes

**FileMap** object can be updated multiple times with content from the
different data folders:

```python
config = FileMap()

config.update('/etc/config')
config.update('/etc/config2')
config.update('/etc/secrets')
```

If the same keys exist in different volumes, newer keys override the older
ones.

### Loading binary data

When argument *raw=True* is used either in constructor or in *update* function,
the data is loaded in binary format.

```python
config = FileMap('/etc/binary-keys', raw=True)
config.update('/etc/binary-keys2', raw=True)
```

## Installation

```shell
pip3 install filemap
```
