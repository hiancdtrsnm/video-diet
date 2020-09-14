from pathlib import Path
import filetype

from ffprobe import FFProbe


def get_codec(path: str):
    try:
        metadata = FFProbe(path)
    except:
        return None
    
    if 'video' in metadata.streams:
        return metadata.video[0].codec_name
    
    return metadata.audio[0].codec_name 


def convertion_path(path: Path, audio:bool ):
    print(audio)
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

def check_ignore(file, ignore_extension:str, ignore_path:str):
    
    if (not (ignore_extension == None) and str(file).lower().endswith(ignore_extension)) or (not (ignore_path == None) and str(ignore_path) in str(file)) :
        typer.secho(f'ignoring: {file}')
        return True
    
    return False                