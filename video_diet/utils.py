from pathlib import Path
import filetype

from ffprobe import FFProbe


def get_codec(path: str):
    try:
        metadata = FFProbe(path)
    except:
        return None
    return metadata.video[0].codec_name

def get_codec_audio(path: str):
    try:
        metadata = FFProbe(path)
    except:
        return None
    return metadata.audio[0].codec_name


def convertion_path(path: Path):

    if path.suffix.lower() not in ['.mkv', '.mp4']:
        return path.parent / (path.stem + '.mkv')

    return path.parent / ('conv-' + path.name)

def convertion_path_audio(path: Path):
    
    if path.suffix.lower() not in ['.aac', '.m4a']:
        return path.parent / (path.stem + '.aac')

    return path.parent / ('conv-' + path.name)



def check_if_video(path: str):

    guess = filetype.guess(path)

    return guess and 'video' in guess
