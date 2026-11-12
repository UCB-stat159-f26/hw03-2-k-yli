import matplotlib.pyplot as plt

def plot_career_matches(matches):
    # Plot a player's age and age gap by match result; return the axes.
    _, ax = plt.subplots(figsize=(12, 7))
    for result, label, color in [("W", "Win", "skyblue"), ("L", "Loss", "purple")]:
        group = matches.loc[matches["result"] == result]
        ax.scatter(group["player_age"], group["age_difference"],
                   label=label, color=color, s=25, linewidths=0)
    ax.axhline(0, color="gray", linewidth=1)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set(xlabel="Player age (years)", ylabel="Player age - opponent age (years)", title="Career matches by age and result")
    ax.set_axisbelow(True)
    ax.grid(alpha=0.3)
    ax.legend(frameon=False)
    return ax
