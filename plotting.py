'''
This module runs everything in election.py, takes the simulation results,
then plot them using altair.
'''

import pandas as pd
import altair as alt
from election import *

# PLOTTING
SYSTEM = ["fptp_winner", "approval_winner", "borda_winner", "score_winner"]
COLOR_NAMES = ["Draw", "Red", "Blue", "Green"]
COLORS = ["#6b6b6b", "red", "#12a9e5", "#12e551"]
COLOR_SCALE = alt.Scale(domain=COLOR_NAMES, range=COLORS)

v_df = pd.DataFrame()
v_df["v_x"] = v_x
v_df["v_y"] = v_y
v_df["fptp_winner"] = fptp_winner
v_df["approval_winner"] = approval_winner
v_df["borda_winner"] = borda_winner
v_df["score_winner"] = score_winner
df = pd.melt(v_df, id_vars=["v_x", "v_y"], var_name="SYSTEM", value_name="winner")

c_df = pd.DataFrame(CAND_DICT)
c_df = pd.concat([c_df, c_df, c_df, c_df], sort=False, ignore_index=True)
c_df["SYSTEM"] = SYSTEM * 3
df = pd.concat([df, c_df], sort=False, ignore_index=True)

candidate_plot = alt.Chart().mark_point(filled=True).encode(
    alt.X('C_X', title="x"),
    alt.Y('C_Y', title="y"),
    alt.Color('name', legend=None, scale=COLOR_SCALE),
    alt.Shape('name', legend=alt.Legend(title="Candidates")),
    opacity=alt.value(1),
    size=alt.value(150)
)

voter_plot = alt.Chart().mark_circle().encode(
    x = 'v_x',
    y = 'v_y',
    color = alt.Color('winner:N', legend=None, scale=COLOR_SCALE)
).properties(
    width=250
)

chart = alt.layer(
    voter_plot,
    candidate_plot,
    data=df
).facet(
    column='SYSTEM:N'
).configure_header(
    labelFontSize=20
)

#chart.save("HTML file path here") 
