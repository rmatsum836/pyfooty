# PyFooty
[![Build Status](https://dev.azure.com/rayamatsumoto/pyfooty/_apis/build/status/rmatsum836.pyfooty?branchName=master)](https://dev.azure.com/rayamatsumoto/pyfooty/_build/latest?definitionId=3&branchName=master)
[![codecov](https://codecov.io/gh/rmatsum836/pyfooty/branch/master/graph/badge.svg)](https://codecov.io/gh/rmatsum836/pyfooty)

<br>

PyFooty is a simple Python package to parse soccer stats from [FBRef](https://fbref.com/en/).
<br/>
Disclaimer: This package is in early stages and API is subject to change.

## Installation
PyFooty can be installed from source by running the following on the command line inside the package: `pip
install -e .`

## Usage
Functionality is currently limited to parsing player stats.  As an example, we will grab the passing stats for
Eden Hazard of Real Madrid.  Start by initializing the `Player` object:
```
from pyfooty.src.player import Player
hazard = Player("Eden Hazard")
```

Then the Passing stats can be grabbed by calling the `get_table()` method:
```
passing = hazard.get_table("Passing")
```
### Acknowledgements
Some code taken from: https://github.com/chmartin/FBref_EPL
