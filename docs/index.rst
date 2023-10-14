.. overwatchpy documentation master file, created by
   sphinx-quickstart on Fri Oct 13 23:30:17 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to overwatchpy's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
    

Installation
============
.. code-block:: bash

    pip install overwatchpy

Usage
=====
.. code-block:: python
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
