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

