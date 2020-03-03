__version__ = '0.0.5'

from pathlib import Path
from types import SimpleNamespace
from pyaltt2.converters import val_to_boolean


def _serialize_ns(ns):
    result = ns.__dict__
    for r, v in result.items():
        if isinstance(v, SimpleNamespace):
            result[r] = _serialize_ns(v)
    return result


class FileMap:

    def __init__(self, path=None, **kwargs):
        """
        Args:
            path: initial import path (optional)
            other kwargs: passed to initial update as-is
        """
        self.data = SimpleNamespace()
        if path: self.update(path, **kwargs)

    def update(self, path, default_type=str, types={}):
        """
        Args:
            path: import path
            default_type: default type
            types: dict of extra types in format:
                    tuple (field, type)
                    e.g.
                    ('somekey', int)
                    valid types: 'int', 'float', 'raw', 'json', 'str', 'bool'
                    built-in types can be used w/o quotes, bytes is equal to
                    'raw'
        """
        src = Path(path)
        if default_type is None:
            default_type = str
        if types is None:
            types = {}
        for p in src.glob('*'):
            if not p.name.startswith('.'):
                d = self.data
                ks = p.name.split('.')
                for z in ks[:-1]:
                    n = getattr(d, z, None)
                    if not isinstance(n, SimpleNamespace):
                        sn = SimpleNamespace()
                        setattr(d, z, sn)
                        n = sn
                    d = n
                ct = types.get(p.name, default_type)
                if ct == 'str':
                    ct = str
                elif ct == 'int':
                    ct = int
                elif ct == 'float':
                    ct = float
                elif ct == 'float':
                    ct = float
                elif ct == 'bool':
                    ct = bool
                elif ct in ['raw', 'bytes']:
                    ct = bytes
                with open(p, 'r' + ('b' if ct is bytes else '')) as fh:
                    value = fh.read()
                    if ct == 'json':
                        import yaml
                        value = yaml.load(value)
                    elif ct is str:
                        value = value.rstrip()
                    elif ct is int:
                        value = int(value)
                    elif ct is float:
                        value = float(value)
                    elif ct is bool:
                        value = val_to_boolean(value.strip())
                    setattr(d, ks[-1], value)

    def __iter__(self):
        for k, v in self.serialize().items():
            yield (k, v)

    def serialize(self):
        return _serialize_ns(self.data)

    def get(self, key, default=AttributeError, _ns=None):
        """
        Args:
            key: key name
            default: default value if key not found
        Raises:
            AttributeError: if default value is not specified
        """
        ns = _ns if _ns else self.data
        try:
            if '.' in key:
                ks = key.split('.', 1)
                return self.get(ks[1], default=default, _ns=getattr(ns, ks[0]))
            else:
                return getattr(ns, key)
        except AttributeError:
            if default is not AttributeError:
                return default
            else:
                raise
