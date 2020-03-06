#pylint: disable=E251, C0103, R1705, C0330

'''
Contains all the functions to generate ballots, calculate winner, detect draws
and zeros. Finally it runs a simulation with a hard-coded number of voters and
number of elections (simulations)

Definitions of essential terms
----------
"Individual voter"
    one single voter that casts their ballot based on the distance between
    them and the candidate.
"A group of voters"
    a collection of multiple of individual voters centered around a given mean
"A set of a voting group"
    a collection of multiple of group of voters
'''

import numpy as np
import pandas as pd
import altair as alt
from tqdm import tqdm

# CANDIDATES
CAND_NAMES = ["Red", "Blue", "Green"]
C_X = np.array([2, -2, 0])
C_Y = np.array([2, 2, -2])

CAND_DICT = {
    "C_X": C_X,
    "C_Y": C_Y,
    "name": CAND_NAMES
}

def counter(system_list):
    '''
    Counts the total number of votes received by each candidate and return a
    winner, or a draw if one is detected

    Parameters
    ----------
    system_list: np.array
        Array of total number of votes for each candidate

    Returns
    -------
    winner: str
       Returns the name of the winning candidate.
    '''
    if system_list.size != 0:
        counts = np.bincount(system_list)
        position = np.where(counts)[0]
        list_of_votes = counts[position]
        # Finds max, random tie break if there is a draw
        max_pos = np.random.choice(np.flatnonzero(list_of_votes == list_of_votes.max()))

        winner_pos = position[max_pos]
        winner = CAND_NAMES[winner_pos]
        return winner
    else: # There are no votes
        winner = "None"
        return winner
##


# ELECTORAL SYSTEM FUNCTIONS
# ===================================================================
def fptp(dist_list): ##
    fptp_votes = np.argmin(dist_list, axis=1)
    f_winner = counter(fptp_votes)
    return f_winner
##


def approval(dist_list): ##
    # TODO: variable approval radius
    APPROVAL_RADIUS = 2
    approved = np.array(np.where(dist_list <= APPROVAL_RADIUS))
    approval_list = approved[1]
    a_winner = counter(approval_list)
    return a_winner
##


def borda(d_sorted): ##
    # FIXME: only works for 3 candidates
    borda_list = np.array(
        [
            np.transpose(np.where(d_sorted == 0))[:, 1],
            np.transpose(np.where(d_sorted == 1))[:, 1],
            np.transpose(np.where(d_sorted == 2))[:, 1],
        ]
    )
    borda_sum = np.sum(borda_list, axis=1)
    borda_winner_pos = np.argmin(borda_sum)
    b_winner = CAND_NAMES[borda_winner_pos]
    return b_winner
##


def score(dist_list): ##
    # TODO: variable radius and score; interprete those as inequalities
    # radius = [0.5, 1, 2, 3]
    # score = [10, 8, 7, 5, 0]
    # Actually makes a new array not replace
    score_list = np.zeros(dist_list.shape)
    np.place(score_list, np.logical_and(dist_list >= 2, dist_list <= 3), [5])
    np.place(score_list, np.logical_and(dist_list >= 1, dist_list <= 2), [7])
    np.place(score_list, np.logical_and(dist_list >= 0.5, dist_list <= 1), [8])
    np.place(score_list, dist_list <= 0.5, [10])

    score_sum = np.einsum('ij->j', score_list)  # Sum all columns
    score_winner_pos = np.random.choice(np.flatnonzero(score_sum == score_sum.max()))
    if score_sum.size != 0:
        winner = CAND_NAMES[score_winner_pos]
        return winner
    else: # There are no votes
        winner = "None"
        return winner
##
# *******************************************************************


# MAIN ELECTION FUNCTION
def election(
        voter_set_x,
        voter_set_y,
        N_VOTER_IN_GROUP,
        STDEV,
        candidate_x=C_X,
        candidate_y=C_Y
): ##
    '''
    Randomly generates a group of voters in a normal distribution,
    then calculate their ballots and return the winner of the election.

    Parameters
    ----------
    voter_set_x, voter_set_y: float
        Provides the x and y means for randomly generating a group of voters
        in a normal distribution
    N_VOTER_IN_GROUP: int
        Number of voters in the voting group to be randomly generated
    STDEV: float or int
        Standard deviation of the normal distribution to be generated
    candidate_x, candidate_y: np.array
         Array of the candidate’s x and y coordinates

    Returns
    -------
    (voter_set_x, voter_set_y, fptp_winner, approval_winner, borda_winner,
    score_winner): tuple
       Returns the names of the winning candidates in every electoral system
       in a tuple. Also returns the coordinates of the voter group in this
       election.
    '''
    #print(voter_set_x, voter_set_y) # Ensure different every loop
    v_x = np.random.normal(voter_set_x, STDEV, N_VOTER_IN_GROUP)
    v_y = np.random.normal(voter_set_y, STDEV, N_VOTER_IN_GROUP)
    #print(v_x)

    # DISTANCE
    diff_x = np.subtract.outer(v_x, candidate_x)
    diff_y = np.subtract.outer(v_y, candidate_y)
    distance_list = np.hypot(diff_x, diff_y)
    #print(d)
    d_sorted = np.argsort(distance_list, axis=1)

    fptp_winner = fptp(distance_list)
    approval_winner = approval(distance_list)
    borda_winner = borda(d_sorted)
    score_winner = score(distance_list)

    #print("FPTP: " + str(fptp_winner))
    #print("Approved: " + str(approval_winner))
    #print("Borda: " + str(borda_winner))
    #print("Score: " + str(score_winner))

    return (
        voter_set_x,
        voter_set_y,
        fptp_winner,
        approval_winner,
        borda_winner,
        score_winner
    )
##


def loop_elections(c_x, c_y):
    N_VOTER_IN_GROUP = 1000
    STDEV = 1

    NUM_OF_ELECTIONS = 10**4 # Only even powers
    result = []

    grid = np.array(
            np.meshgrid(
                    np.linspace(-2, 2, int(np.sqrt(NUM_OF_ELECTIONS))),
                    np.linspace(-2, 2, int(np.sqrt(NUM_OF_ELECTIONS)))
            )).T.reshape(-1,2).T

    with tqdm(total=NUM_OF_ELECTIONS) as pbar:
        loop_number = 0
        while loop_number < NUM_OF_ELECTIONS: ##
            result.append(
                election(
                    grid[0][loop_number],
                    grid[1][loop_number],
                    N_VOTER_IN_GROUP,
                    STDEV,
                    candidate_x=c_x,
                    candidate_y=c_y
                )
            )
            pbar.update(1)
            loop_number += 1
    ##
    v_x, v_y, fptp_winner, approval_winner, borda_winner, score_winner = zip(*result)
    return (v_x, v_y, fptp_winner, approval_winner, borda_winner, score_winner)

def plotter(v_x, v_y, fptp_winner, approval_winner, borda_winner, score_winner):
    SYSTEM = ["fptp_winner", "approval_winner", "borda_winner", "score_winner"]
    COLOR_NAMES = ["Draw", "Red", "Blue", "Green"]
    COLORS = ["#6b6b6b", "red", "#12a9e5", "#12e551"]
    COLOR_SCALE = alt.Scale(domain=COLOR_NAMES, range=COLORS)

    v_df = pd.DataFrame({
        "v_x": v_x,
        "v_y": v_y,
        "fptp_winner": fptp_winner,
        "approval_winner": approval_winner,
        "borda_winner": borda_winner,
        "score_winner": score_winner
    })
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
        alt.StrokeValue("black"),
        opacity=alt.value(1),
        size=alt.value(150)
    )

    voter_plot = alt.Chart().mark_circle().encode(
        x = 'v_x',
        y = 'v_y',
        color = alt.Color('winner:N', legend=None, scale=COLOR_SCALE)
    ).properties(
        width=200
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

    return chart
# End function


alt.data_transformers.disable_max_rows()
def plot():
    v_x, v_y, fptp_winner, approval_winner, borda_winner, score_winner = loop_elections(C_X, C_Y)
    chart = plotter(v_x, v_y, fptp_winner, approval_winner, borda_winner, score_winner)
    print("Please wait...")
    chart.save('chart.png', webdriver='firefox')

plot()
