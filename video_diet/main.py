import typer
from pathlib import Path
import filetype
import os
import shutil
from typer.colors import RED, GREEN
import enlighten
import ffmpeg
from .utils import convertion_path, get_codec, check_ignore
from . import convert_file, convert_video_progress_bar

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

    manager = enlighten.get_manager()
    errors_files = []
    pbar = manager.counter(total=len(videos)+len(audios), desc='Files', unit='files')

    for video in videos:
        typer.secho(f'Processing: {video}')
        if get_codec(str(video)) != 'hevc':
            new_path = convertion_path(video, False)

            if new_path.exists():
                os.remove(str(new_path))

            try:
                convert_video_progress_bar(str(video), str(new_path), manager)
                os.remove(str(video))
                if video.suffix == new_path.suffix:
                    shutil.move(new_path, str(video))

            except ffmpeg._run.Error:
                typer.secho(f'ffmpeg could not process: {str(video)}', fg=RED)
                errors_files.append(video)

        pbar.update()

    for audio in audios:
        typer.secho(f'Processing: {audio}')
        if get_codec(str(audio)) != 'hevc':

            new_path = convertion_path(audio, True)

            if new_path.exists():
                os.remove(str(new_path))

            try:

                convert_file(str(audio),str(new_path))

                os.remove(str(audio))
                if audio.suffix == new_path.suffix:
                    shutil.move(new_path, str(audio))

            except ffmpeg._run.Error:
                typer.secho(f'ffmpeg could not process this file: {str(audio)}', fg=RED)
                errors_files.append(audio)


        pbar.update()

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
), force: bool = typer.Option(
    default=False,
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


    if get_codec(str(path)) == 'hevc' and not force:
        typer.secho('This video codec is already \'hevc\'', fg=GREEN)
        return

    try:
        convert_video_progress_bar(str(path), str(conv_path))

    except FileNotFoundError as error:
        if error.filename == 'ffmpeg':
            readme_url = 'https://github.com/hiancdtrsnm/video-diet#FFMPEG'
            typer.secho('It seems you don\'t have ffmpeg installed', fg=RED)
            typer.secho(f'Check FFMPEG secction on {readme_url}', fg=RED)
        else:
            raise error
