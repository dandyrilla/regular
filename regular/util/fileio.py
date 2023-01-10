import os
import json

import pandas as pd


def make_parent_dir(path):
    parent_dir = os.path.normpath(os.path.dirname(path))
    is_root_dir = (parent_dir == os.path.sep)
    is_current_dir = (parent_dir == '.')
    if not (is_root_dir or is_current_dir):
        os.makedirs(parent_dir, exist_ok=True)


def write(out, filename, mode='w'):
    """Write text into a file."""
    make_parent_dir(filename)
    with open(filename, mode) as f:
        f.write(out)


def to_tsv(df, tsvfile, **kw):
    make_parent_dir(tsvfile)
    _kw = dict(sep='\t', index=False)
    _kw.update(kw)
    df.to_csv(tsvfile, **_kw)


def read_tsv(tsvfile, **kw):
    _kw = dict(sep='\t', header=0)
    _kw.update(kw)
    df = pd.read_csv(tsvfile, **_kw)
    return df


def json_load(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def json_dump(data, filename, **kw):
    make_parent_dir(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, **kw)
