import re
from pathlib import Path
import filetype
import typer

from .patch_ffprobe import FFProbe

px10bit = re.compile('10le$')
px12bit = re.compile('12le$')

class PixelFormat:
    __slots__ = ('_px_format', '_is_10bit', '_is_12bit')
    def __init__(self, px_format):
        self._px_format = px_format
        self._is_10bit = px10bit.search(px_format) is not None
        self._is_12bit = px12bit.search(px_format) is not None

    @property
    def pixel_format(self):
        return self._px_format

    @property
    def is_10bit(self):
        return self._is_10bit

    @property
    def is_12bit(self):
        return self._is_12bit

    @property
    def is_8bit(self):
        return not(self._is_10bit or self._is_12bit)

    def __str__(self):
        return self._px_format



def get_codec(path: str):
    try:
        metadata = FFProbe(path)
    except:
        return None

    if len(metadata.video) != 0:
        return metadata.video[0].codec()

    return metadata.audio[0].codec()

def get_bitdepth(path: str):
    try:
        metadata = FFProbe(path)
    except:
        return None

    if len(metadata.video) != 0:
        pixel_format = metadata.video[0].pixel_format()
        return PixelFormat(pixel_format)

    return None

def convertion_path(path: Path, audio: bool ):

    if not audio:

        if path.suffix.lower() not in ['.mkv', '.mp4']:

            return path.parent / (path.stem + '.mkv')

    else:

        if path.suffix.lower() not in ['.aac', '.m4a']:

            return path.parent / (path.stem + '.aac')

    return path.parent / ('conv-' + path.name)



def check_if_video(path: str):

    guess = filetype.guess(path)

    return guess and 'video' in guess

def check_ignore(file_path, ignore_extension:str, ignore_path:str):

    ignored_by_extension = ignore_extension is not None \
        and str(file_path).lower().endswith(ignore_extension)
    ignored_by_path = ignore_path is not None \
        and str(ignore_path) in str(file_path)

    if ignored_by_extension or ignored_by_path:
        typer.secho(f'Ignoring: {file_path}')
        return True

    return False
