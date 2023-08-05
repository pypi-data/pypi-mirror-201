# Note

This repo is based on the excellent tool by @aantn: https://github.com/aantn/reconstant

# Introduction
ConstGen lets you share multiple object definitions between multiple programming languages:

* constants
* enums
* types

Supported Languages:

* Rust
* Javascript
* Go
* Java
* C/CPP
* Python2/3
* Vue

## Installation
```
pip install git+https://github.com/ymec/constgen.git
```
OR
```
pip install constgen
```

## Usage
Create a configuration yaml (for an example see `example.yaml`)

```
constgen example.yaml
```

# Known Issues

Currently running main only works through pip installing the tool - running directly with python would cause import errors
