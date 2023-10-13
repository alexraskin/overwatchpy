# OverwatchPy

A Python wrapper for [https://overfast-api.tekrop.fr/](https://overfast-api.tekrop.fr/)

I wrote this very fast so it's not very good, but it works.

Please open a PR if you want to improve it or add more features.

## Requirements

- Python 3.11 (3.9+ should work)
- Poetry

## Installation

```bash
poetry install
```

## Usage

```python
from overwatchpy import Overwatch

search: Overwatch.player_search = Overwatch.player_search("twizy", "quickplay", "pc", "public")

for player in search:
    print(player.name)

ow = Overwatch(battletag="Twizy#11358", gamemode="quickplay", platform="pc")

print(ow.maps())
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
