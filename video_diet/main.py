from typing import Optional
import typer
from pathlib import Path
import filetype
import os
import shutil
from typer.colors import RED
import enlighten

from .utils import convertion_path, get_codec
from . import convert_video

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def folder(path: Path = typer.Option(
    default='.',
    exists=True,
    file_okay=True,
    dir_okay=True,
    readable=True,
    resolve_path=True
)):
    """
    Convert all videos in a folder
    """

    videos = []

    for dir, folders, files in os.walk(path):
        base_dir = Path(dir)
        for file in files:
            file = base_dir / file
            guess = filetype.guess(str(file))

            if guess and 'video' in guess.mime:
                videos.append(file)

    manager = enlighten.get_manager()
    pbar = manager.counter(total=len(videos), desc='Video', unit='videos')
    for video in videos:
        typer.secho(f'Processing: {video}')
        if get_codec(str(video)) != 'hevc':
            new_path = convertion_path(video)
            convert_video(str(video),str(new_path))
            os.remove(str(video))
            shutil.move(new_path, str(video))
        pbar.update()

@app.command()
def file(path: Path = typer.Option(
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
        typer.secho('Please write the video path', fg=RED)
        return


    conv_path = convertion_path(path)

    if conv_path.exists():
        typer.secho('The destination file already exist, please delete it', fg=RED)
        return

    convert_video(str(path),str(conv_path))
