# mkie

A useful tool for control clis in terminal.

## Installation

If you already know how to install python packages, then you can install it via pip.

```
pip3 install mkie
```

## Upgrade

```
pip3 install --upgrade mkie
```

## Features

`mkie` is control clis:

- Git
  - `gitadd`: Auto add all files to git and ignore submodules.
  - `gitfetch`: Sort out local branchs.
  - `gitpull`: Pull latest update from git repo.
  - `s`: Swap current branch to target branch.

- Docker
  - `dps`: list docker containers 
  - `dbu`: build docker container
  - `dup`: start docker contrainer
  - `dd`: stop docker container
  - `drun`: exec docker container
