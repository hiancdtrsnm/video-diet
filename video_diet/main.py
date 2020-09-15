from typing import List
import typer
from pathlib import Path
import filetype
import os
import shutil
from typer.colors import RED, GREEN
import enlighten
import ffmpeg

from .utils import convertion_path, get_codec, check_ignore
from . import convert_file

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def folder(path: Path = typer.Argument(
    default='.',
    exists=True,
    file_okay=True,
    dir_okay=True,
    readable=True,
    resolve_path=True
), ignore_extension: str = typer.Option(
    default=None
), ignore_path: Path = typer.Option(
    default=None,
    exists=True,
    file_okay=True,
    dir_okay=True,
    readable=True,
    resolve_path=True
)):
    """
    Convert all videos and audios in a folder
    """

    videos, audios = get_videos_and_audios(path, ignore_extension, ignore_path)  
    manager = enlighten.get_manager()
    errors_files = []
    pbar = manager.counter(total=len(videos)+len(audios), desc='Files', unit='files')
    
    errors_files, pbar = process_files(videos, False, errors_files, pbar)
    errors_files, pbar = process_files(audios, True, errors_files, pbar)

    if errors_files:
        typer.secho('This videos could not be processed:', fg=RED)
        typer.secho(str(errors_files), fg=RED)


@app.command()
def file(path: Path = typer.Argument(
    default=None,
    exists=True,
    file_okay=True,
    dir_okay=False,
    readable=True,
    resolve_path=True
)):
    """
    Convert a file
    """

    if path is None:
        typer.secho('Please write the video or audio path', fg=RED)
        return

    guess = filetype.guess(str(path))
    
    if guess and 'video' in guess.mime:
        conv_path = convertion_path(path, False)
    else:
        conv_path = convertion_path(path, False)

    if conv_path.exists():
        typer.secho('The destination file already exist, \
                    please delete it', fg=RED)
        return


    if get_codec(str(path)) == 'hevc':
        typer.secho('This video codec is already \'hevc\'', fg=GREEN)
        return

    try:
        convert_file(str(path), str(conv_path))

    except FileNotFoundError as error:
        if error.filename == 'ffmpeg':
            readme_url = 'https://github.com/hiancdtrsnm/video-diet#FFMPEG'
            typer.secho('It seems you don\'t have ffmpeg installed', fg=RED)
            typer.secho(f'Check FFMPEG secction on {readme_url}', fg=RED)
        else:
            raise error


def get_videos_and_audios(path: Path, ignore_extension: str, ignore_path: Path):
    videos = []
    audios = []

    for dir, folders, files in os.walk(path):
        base_dir = Path(dir)
        for item in files:

            file_path = base_dir / item
            guess = filetype.guess(str(file_path))

            if check_ignore(file_path, ignore_extension, ignore_path):
                continue
            
            if guess and 'video' in guess.mime : 
                
                videos.append(file_path)
            
            if guess and 'audio' in guess.mime:
                
                audios.append(file_path)   

    return videos, audios 


def process_files(files: List, is_audio: bool, errors_files: List, pbar):
    for file in files:
        typer.secho(f'Processing: {file}')
        if get_codec(str(file)) != 'hevc':
            new_path = convertion_path(file, is_audio)

            try:

                convert_file(str(file),str(new_path))

                os.remove(str(file))
                if file.suffix == new_path.suffix:
                    shutil.move(new_path, str(file))

            except ffmpeg._run.Error:
                typer.secho(f'ffmpeg could not process: {str(file)}', fg=RED)
                errors_files.append(file)

        pbar.update()
    
    return errors_files, pbar