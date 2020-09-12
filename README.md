# Video diet

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?label=license)](https://www.gnu.org/licenses/gpl-3.0) [![Last commit](https://img.shields.io/github/last-commit/hiancdtrsnm/video-diet.svg?style=flat)](https://github.com/hiancdtrsnm/video-diet/commits) [![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hiancdtrsnm/video-diet)](https://github.com/hiancdtrsnm/video-diet/commits) [![Github Stars](https://img.shields.io/github/stars/hiancdtrsnm/video-diet?style=flat&logo=github)](https://github.com/hiancdtrsnm/video-diet) [![Github Forks](https://img.shields.io/github/forks/hiancdtrsnm/video-diet?style=flat&logo=github)](https://github.com/hiancdtrsnm/video-diet) [![Github Watchers](https://img.shields.io/github/watchers/hiancdtrsnm/video-diet?style=flat&logo=github)](https://github.com/hiancdtrsnm/video-diet) [![GitHub contributors](https://img.shields.io/github/contributors/hiancdtrsnm/video-diet)](https://github.com/hiancdtrsnm/video-diet/graphs/contributors)

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

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

Good luck 😉.

Project Structure based on awesome tutorial by @tiangolo at https://typer.tiangolo.com/tutorial/package

https://ffmpeg.org/download.html
