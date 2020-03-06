# Electoral Systems

![Preview](https://raw.githubusercontent.com/yc-tsui/electoral-systems/master/chart.png)

Simulates virtual elections using different electoral systems, with voters and candidates on a 2D plane.

Inspired by Ka Yee-Ping's [Voting Simulation Visualizations](http://zesty.ca/voting/sim/) and Nicky Case's [To build a better ballot](https://ncase.me/ballot/)


## Usage (with .py file)

0. Install all the requirements (see [Prerequisities](https://github.com/yc-tsui/electoral-systems#prerequisites))
1. Familiarize yourself with the terminology used (in `election.py`)
2. In `election.py`, change the values of the constants (in ALLCAPS) to suit yourself
3. Change your desired output path
4. Run `election.py`.

## Depreciated usage (with Jupyter notebook for interactive movable candidates) (no longer works)

Note: latest Jupyter notebook not updated, because the newest version uses 10^4 values so the Jupyter notebook is a few MB large. Also ipyvega removed notebook support (for Jupyterlab support?)

1. Open the Binder page [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yc-tsui/electoral-systems/master)
2. Run all cells
3. Drag the sliders to move each candidate's `x` and `y` coordinates

In the Jupyter version of the code, `plotting.py` is made into a separate function. That could be useful for max modularity.


## Prerequisites

[Altair](http://altair-viz.github.io/) is used instead of the "usual" matplotlib. I find its syntax much better than matplotlib. For and while loops should never be used, and declarative programming is how we should be plotting graphs.

~~Altair also requires `pyvega` to be installed for juypter notebook.~~ See [requirements.txt](https://github.com/yc-tsui/electoral-systems/blob/master/requirements.txt)
