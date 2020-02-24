__version__ = '0.0.1'

from pathlib import Path
from types import SimpleNamespace


def _serialize_ns(ns):
    result = ns.__dict__
    for r, v in result.items():
        if isinstance(v, SimpleNamespace):
            result[r] = _serialize_ns(v)
    return result


class FileMap:

    def __init__(self, path=None, allow_empty=False, raw=False):
        if path: self.update(path, raw=raw)
        self.allow_empty = allow_empty

    def update(self, path, raw=False):
        self.data = SimpleNamespace()
        src = Path(path)
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
                with open(p, 'r' + ('b' if raw else '')) as fh:
                    value = fh.read()
                    if not raw: value = value.rstrip()
                    setattr(d, ks[-1], value)

    def serialize(self):
        return _serialize_ns(self.data)

    def get(self, key, _ns=None):
        ns = _ns if _ns else self.data
        try:
            if '.' in key:
                ks = key.split('.', 1)
                return self.get(ks[1], getattr(ns, ks[0]))
            else:
                return getattr(ns, key)
        except AttributeError:
            if self.allow_empty: return None
            else: raise
