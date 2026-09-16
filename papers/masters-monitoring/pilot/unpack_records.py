#!/usr/bin/env python3
"""Expand frozen numerical/reference records. Never downloads or copies images."""
from pathlib import Path
import zipfile

def unpack():
    root=Path(__file__).resolve().parent
    with zipfile.ZipFile(root/'records.zip') as bundle:
        for item in bundle.infolist():
            dest=(root/item.filename).resolve()
            if root not in dest.parents or item.is_dir():
                raise ValueError('Unexpected archive entry: '+item.filename)
            data=bundle.read(item)
            if dest.exists() and dest.read_bytes()!=data:
                raise FileExistsError('Refusing to replace different records: '+str(dest))
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
    return root

if __name__=='__main__':
    print('Frozen records available at',unpack())
