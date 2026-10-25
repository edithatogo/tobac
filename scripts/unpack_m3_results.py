"""Restore losslessly packed M3 outputs; standard library, bounded and fail-closed."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import lzma
from pathlib import Path, PurePosixPath
import tarfile

MAX_BYTES=5_000_000


def safe_members(raw: bytes) -> dict[str, bytes]:
    if len(raw)>MAX_BYTES:raise ValueError('Unpacked archive exceeds the bounded result contract')
    files={}
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as archive:
        for member in archive:
            path=PurePosixPath(member.name)
            if (not member.isfile() or path.is_absolute() or len(path.parts)!=2
                    or path.parts[0] not in {'full','refined'} or '..' in path.parts
                    or path.suffix not in {'.csv','.json'} or member.name in files
                    or member.size<0 or member.size>MAX_BYTES):
                raise ValueError('Unsafe or duplicate archive member')
            source=archive.extractfile(member)
            if source is None:raise ValueError('Missing member bytes')
            files[member.name]=source.read(MAX_BYTES+1)
            if len(files[member.name])!=member.size:raise ValueError('Truncated member')
    if sum(map(len,files.values()))>MAX_BYTES:raise ValueError('Expanded output exceeds limit')
    return files


def unpack(source: Path, destination: Path) -> int:
    source,destination=Path(source),Path(destination)
    if destination.exists():raise FileExistsError('Use a new output directory')
    manifest=json.loads((source/'manifest.json').read_text())
    if manifest['schema']!='tobac.m3.saved-runs.v1':raise ValueError('Unknown archive schema')
    pieces=[]
    for part in manifest['parts']:
        name=part['name']
        if name not in {'part-001','part-002','part-003'}:raise ValueError('Invalid part path')
        data=(source/name).read_bytes()
        if len(data)!=part['size'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
            raise ValueError('Archive part mismatch')
        pieces.append(data)
    packed=b''.join(pieces)
    if (len(packed)>MAX_BYTES or len(packed)!=manifest['archive_bytes']
            or hashlib.sha256(packed).hexdigest()!=manifest['archive_sha256']):
        raise ValueError('Complete archive mismatch')
    decoder=lzma.LZMADecompressor(memlimit=128*1024*1024)
    raw=decoder.decompress(packed,max_length=MAX_BYTES+1)
    if not decoder.eof or decoder.unused_data:raise ValueError('Oversized or trailing archive stream')
    files=safe_members(raw)
    if len(files)!=manifest['file_count']:raise ValueError('Archive file-count mismatch')
    destination.mkdir(parents=True,exist_ok=False)
    for name,data in files.items():
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as handle:handle.write(data)
    return len(files)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
    parser.add_argument('--archive',default='results/milestone3/archive');args=parser.parse_args()
    print(json.dumps({'restored_files':unpack(Path(args.archive),Path(args.out)),
                      'scope':'saved conditional outputs, not new observed evidence'}))

if __name__=='__main__':main()
