
# pokepastes-scraper

A simple library that converts a Pokemon team from https://pokepast.es to an object in Python.

### Installation

`pip install -U pokepastes-scraper`

### Usage 

Let's say we want to parse [this team](https://pokepast.es/5c46f9ec443664cb) which Gavin Michaels used to win the [Oceania World Championships](https://victoryroadvgc.com/2023-ocic/). Simply call `team_from_url`:

```python
import pokepastes_scraper as pastes

team = pastes.team_from_url("https://pokepast.es/5c46f9ec443664cb")

for mon in team.members:
    print(f"{mon.species} with {mon.item}")
```

Output: 

```
Iron Hands with Assault Vest
Amoonguss with Sitrus Berry
Pelipper with Focus Sash
Palafin with Mystic Water
Baxcalibur with Dragon Fang
Dragonite with Lum Berry
```

For a detailed example output of `team_from_url`, see `test/example.py` and its output `test/example_team.json`.

Tested in python 3.11, but likely compatible with 3.7+. Feel freet to contact me about functionality you would like implemented.