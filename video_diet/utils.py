from pathlib import Path
import filetype
import typer

from ffprobe import FFProbe


def get_codec(path: str):
    try:
        metadata = FFProbe(path)
    except:
        return None

    if 'video' in metadata.streams:
        return metadata.video[0].codec_name

    return metadata.audio[0].codec_name


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
