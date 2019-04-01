# Electoral Systems [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yc-tsui/electoral-systems/master)

![Preview](https://raw.githubusercontent.com/yc-tsui/electoral-systems/master/example_output.png)

Simulates virtual elections using different electoral systems, with voters and candidates on a 2D plane.

Inspired by Ka Yee-Ping's [Voting Simulation Visualizations](http://zesty.ca/voting/sim/) and Nicky Case's [To build a better ballot](https://ncase.me/ballot/)


## Usage (with Juypter notebook for interactive movable candidates)

1. Open the Binder page [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yc-tsui/electoral-systems/master)
2. Run all cells
3. Drag the sliders to move each candidate's `x` and `y` coordinates

In the Juypter version of the code, `plotting.py` is made into a separate function. That could be useful for max modularity.


## Usage (with .py file)

1. Familiarize yourself with the terminology used (in `election.py`)
2. In `election.py`, change the values of `N_VOTER_IN_GROUP` and `NUM_OF_ELECTIONS` to suit yourself
    - Optional: change the coordinates of the candidates in `C_X` and `C_Y`
3. In `plotting.py`, add the path name for your desired html output
4. Run `plotting.py`. It will run election.py, plot the results and save it in your html file


## Prerequisites

[Altair](http://altair-viz.github.io/) is used instead of the "usual" matplotlib. I find its syntax much better than matplotlib. Declarative programming is how we should be plotting graphs.

Altair also requires `pyvega` to be installed for juypter notebook. See [requirements.txt](https://github.com/yc-tsui/electoral-systems/blob/master/requirements.txt)
