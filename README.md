# HW3: Tennis Career Matches

Author: Kristen Li  
Project started: Nov 7 2026

## About the project

`tennis_career` is a Python package that retrieves a player's career match data from [Tennis Abstract](https://www.tennisabstract.com/) and creates a scatter plot based on the one I reproduced in HW2. It provides two public functions:

- `get_career_matches(player_name)` downloads and cleans a player's career match data, then returns it as a pandas DataFrame.
- `plot_career_matches(matches)` uses that DataFrame to create a scatter plot.

In the plot, each point represents one match. The x-axis shows the player's age at the time of the match, and the y-axis shows the player's age minus the opponent's age, in years. Points above zero are matches against younger opponents, and points below zero are matches against older opponents. Blue points represent wins, and purple points represent losses.

## Installation

Install the package from GitHub:

```bash
python -m pip install "git+https://github.com/UCB-stat159-f26/hw03-2-k-yli.git"
```

## Usage

```python
import matplotlib.pyplot as plt
from tennis_career import get_career_matches, plot_career_matches

matches = get_career_matches("Serena Williams")
print(matches.head())

ax = plot_career_matches(matches)
plt.show()
```

`get_career_matches()` takes a player's name and returns a pandas DataFrame. It needs an internet connection to retrieve the data. To try another player, replace `"Serena Williams"` with `"Rafael Nadal"`. `plot_career_matches()` takes the resulting DataFrame and returns a Matplotlib axes object.

## Tests

In your terminal, run these commands from the main folder of this repository:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

The tests use saved sample JS files and run without contacting Tennis Abstract. They check how the package handles opponent birth dates in WTA data, numeric opponent ages in ATP data, and a file that is missing its match array.

