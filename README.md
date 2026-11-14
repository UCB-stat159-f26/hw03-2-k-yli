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

## Reflection

In HW2, I only needed my scripts to make one plot for Serena Williams. When I turned them into a package, I started thinking about what someone else might want to do with the code. For example, they might want to look at the match data before making a plot. I separated the functions so someone could download and clean the data, look through the DataFrame, and then decide whether to plot it. I also learned what `pyproject.toml` does: it tells `pip` how to install the package and which libraries it needs.

One detail I hadn't considered in HW2 was that Tennis Abstract stores opponents' ages differently for the WTA and ATP. For Serena Williams, I had to calculate the opponent's age from their birth date and the match date. For Rafael Nadal, the file already gave me the opponent's age. Once both were in years, I could use the same plotting function. I used small local JavaScript files to check both cases, including the age difference in the first match in my Serena test file. That meant I could run the tests again after a change without downloading the data every time. I used live requests separately to check that the download and plot worked together.

This assignment also helped me put into practice something we’ve emphasized throughout the course: using Git to document how a project came together, using detailed commits for every step of progress. For example, I committed the basic scatter plot first so I could check that it showed the right ages and distinguished wins from losses. Then I applied the HW2 graph styling in a separate commit. If something looked wrong after the styling change, I had a working version to compare it with and a smaller set of changes to inspect. On future projects, I want to continue to use that same rule: commit when I can explain what changed and how I checked it. I would use the same approach on future projects, especially when someone else needs to review or build on my work.