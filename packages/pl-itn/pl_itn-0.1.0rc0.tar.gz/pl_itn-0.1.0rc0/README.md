# pl_itn
Inverse Text Normalization is an NLP task of changing the spoken form of a phrase to written form, for example:
```
one two three -> 1 2 3
```

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

`pl_itn` is an opensource Polish ITN Python library and REST API for practical applications.

This project is an implementation of [NeMo Inverse Text Normalization](https://arxiv.org/abs/2104.05055) for Polish.

## Table of contents
[Prerequisites](#prerequisites)\
[Setup](#setup)\
[Usage](#usage)\
[Documentation](#documentation)\
[Contributing](#contributing)\
[License](#License)\
[References](#References)

## Prerequisites
For [pynini](https://pypi.org/project/pynini/)
- A standards-compliant C++17 compiler (GCC >= 7 or Clang >= 700)
- The compatible recent version of OpenFst built with the grm extensions (see `deps/install_openfst.md`)

## Setup
Make sure to first install prerequisites, especially OpenFST.

### Install from PyPI
```bash
pip install pl_itn
```

### Build from source
```bash
pip install .
```

### Editable install for development
```bash
pip install -e .[dev]
```

## Usage
### Console app
```bash
usage: pl_itn [-h] (-t TEXT | -i) [--tagger TAGGER] [--verbalizer VERBALIZER] [--config CONFIG]
              [--log_level {debug,info}] [-d]

Inverse Text Normalization based on Finite State Transducers

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Input text
  -i, --interactive     If used, demo will process phrases from stdin interactively.
  --tagger TAGGER
  --verbalizer VERBALIZER
  --config CONFIG       Optionally provide yaml config with tagger and verbalizer paths.
  --log_level {debug,info}
  -d, --debug_mode      If used, process will be interrupted on runtime errors, else it will
                        return a step back value.
```

```bash
pl_itn -t "jest za pięć druga"
jest 01:55

pl_itn -t "drugi listopada dwa tysiące osiemnastego roku"
2 listopada 2018 roku
```

### Python
```python
>>> from pl_itn import Normalizer
>>> normalizer = Normalizer()
>>> normalizer.normalize("za pięć dwunasta")
'11:55'
```


## Documentation

## Contributing

## License

## Rerences
- K. Gorman. 2016. Pynini: A Python library for weighted finite-state grammar compilation. In Proc. ACL Workshop on Statistical NLP and Weighted Automata, 75-80.
- Y. Zhang, E. Bakhturina, K. Gorman, and B. Ginsburg. 2021. NeMo Inverse Text Normalization: From Development To Production.