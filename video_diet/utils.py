from pathlib import Path
import filetype

from ffprobe import FFProbe


def get_codec(path: str):
    try:
        metadata = FFProbe(path)
    except:
        return None
    return metadata.video[0].codec_name


def convertion_path(path: Path):

    return path.parent / ('conv-' + path.name)


def check_if_video(path: str):

    guess = filetype.guess(path)

    return guess and 'video' in guess
