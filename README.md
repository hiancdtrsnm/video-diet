# Video diet

This project aims to reduce the spaces of your videos enconding it on hevc.

## For developers

### You must first install *poetry*

Poetry provides a custom installer that will install `poetry` isolated from the rest of your system by vendorizing its dependencies. This is the recommended way of installing `poetry`.

**osx / linux / bashonwindows install instructions**

`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`

**windows powershell install instructions**

`(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python`

The installer installs the `poetry` tool to Poetry's `bin` directory. On Unix it is located at `$HOME/.poetry/bin` and on Windows at `%USERPROFILE%\.poetry\bin`.

This directory will be in your `$PATH` environment variable, which means you can run them from the shell without further configuration.

### Then you need to configure the environment

Inside the project make `poetry install` and after `poetry shell` for start the virtualenv.

For testing the code run `video-diet`.

Good luck 😉.

Project Structure based on awesome tutorial by @tiangolo at https://typer.tiangolo.com/tutorial/package

https://ffmpeg.org/download.html
