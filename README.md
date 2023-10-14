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

client = Overwatch()

heros = client.heroes(role="tank")
for hero in heros:
  print(hero.name)

game_modes = client.gamemodes()
for game_mode in game_modes:
  print(game_mode.name)
  print(game_mode.description)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
