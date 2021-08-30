# CLabel

CLabel is a terminal-based cluster labeling tool that allows you to explore text data interactively and label clusters based on reviewing that data.

## Install & Quickstart

```
pip install clabel
```

Type `clabel` to run. Everything should happen in the terminal from there.

Currently `clabel` can only import CSV files. It expects two columns to be in your csv: a column of text (`string`) and a column of cluster labels (`int`). You'll identify these the first time you import a dataset.

The workflow is:
1. Pick a cluster to view examples. You'll view this through a pager so you can page through examples.
2. Come up with a name for that cluster (`Declare Name`)
3. Repeat 1 & 2 until all your clusters have names.

You can persist any cluster labels to a `json` file when you exit, so you don't have to complete labeling in one session. Then, you can load those labels in the next time you start `clabel` by selecting that `json` file and continue labeling.

## Screenshots

![Pager of Examples](https://i.ibb.co/SwkPHBP/Screen-Shot-2021-08-30-at-4-41-14-PM.png)
![Declaring name of a cluster](https://i.ibb.co/9cM9Q5G/Screen-Shot-2021-08-30-at-4-42-11-PM.png)
![Naming Autocomplete](https://i.ibb.co/rF5qKPN/Screen-Shot-2021-08-30-at-4-41-49-PM.png)
