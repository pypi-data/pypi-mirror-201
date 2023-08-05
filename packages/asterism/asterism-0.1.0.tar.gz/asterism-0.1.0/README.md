# asterism

Helpers and common patterns used in Project Electron infrastructure. This package is named after a pattern or group of stars that is visually obvious, but not officially recognized as a constellation. Read more about asterisms on [Wikipedia](https://en.wikipedia.org/wiki/Asterism_(astronomy)).

[![Build Status](https://app.travis-ci.com/RockefellerArchiveCenter/asterism.svg?branch=base)](https://app.travis-ci.com/RockefellerArchiveCenter/asterism)

## Setup

Make sure this library is installed:

    $ pip install asterism


## Usage

You can then use `asterism` in your Python scripts and applications by importing it:

    import asterism

### What's here

`bagit_helpers` - contains generic bagit functions to validate and update bags.
`file_helpers` - generic functions for manipulating files and directories, as well as working with ZIP and TAR files.
`models` - a `BasePackage` abstract base model that represents a bag of archival records.
`views` - a `BaseServiceView` and a `RoutineView` which provide abstract wrapping methods for handling JSON requests and responses.


## Development
This repository contains a configuration file for git [pre-commit](https://pre-commit.com/) hooks which help ensure that code is linted before it is checked into version control. It is strongly recommended that you install these hooks locally by installing pre-commit and running `pre-commit install`.


## License

This code is released under an [MIT License](LICENSE).
