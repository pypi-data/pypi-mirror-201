# halig

![PyPI](https://img.shields.io/pypi/v/halig?logo=python)
![PyPI - License](https://img.shields.io/pypi/l/halig)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/halig)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

[(R)age](https://github.com/woodruffw/pyrage) encrypted note-taking CLI app.

`halig` opens, using your favorite `$EDITOR`, an in-memory copy of a file and upon save-and-exit,
it encrypts the new contents into an [age](https://github.com/FiloSottile/age) file that
you can store, _relatively_ safe, anywhere.

## Install

```shell
pipx install halig # or pip
```


## Setup TLDR

```shell
set -e
ssh-keygen -t ed25519
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/halig"
cat << EOF > "${XDG_CONFIG_HOME:-$HOME/.config}/halig/halig.yml"
---
notebooks_root_path: /home/$(id -un)/Documents/Notebooks
identity_path: /home/$(id -un)/.ssh/id_ed25519
recipient_path: /home/$(id -un)/.ssh/id_ed25519.pub
EOF
```

## Usage TLDR

```shell
halig edit some_notebook     # edit today's note relative to <notebooks_root_path>/some_notebook
halig edit some_notebook/foo # edit  <notebooks_root_path>/some_notebook/foo.age
halig notebooks              # list current notebooks
```