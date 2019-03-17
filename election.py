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

# Error handling
class ZeroException(Exception): pass
class DrawException(Exception): pass
class NoDrawException(Exception): pass


# BALLOT CALCULATOR FUNCTIONS
# ===================================================================
# Draw checker
def draw_checker(list_of_votes, max_pos): ##
    '''
    Check if there is a draw or zero by raising exceptions

    Parameters
    ----------
    list_of_votes: np.array
        Total number of votes for each candidate
    max_pos: int
        Position of the maximum number in list, equal to position of candidate
        with the most votes.

    Returns
    -------
    NoReturn
        This function only raises draw or zero exceptions

    Raises
    ------
    ZeroException
        The total number of votes for every single candidate is zero
    DrawException
        There are at least two candidates with the same number of votes
    NoDrawException
        There is no zero or draw exception.
    '''
    maximum = list_of_votes[max_pos]
    search = np.where(list_of_votes == maximum)[0]
    if len(search) > 1:
        if list_of_votes[max_pos] == 0:
            raise ZeroException("There is a zero")
        else:
            raise DrawException("There is a draw")
    else:
        raise NoDrawException()
##


def winner_calc(list_of_votes, max_pos, position): ##
    '''
    First check for draws, then returns the winning candidate or a draw

    Parameters
    ----------
    list_of_votes: np.array
        Array of total number of votes for each candidate
    max_pos: int
        Position of the maximum number in list -- position of candidate with
        the most votes.
    position: np.array
        The positions of all candidates ordered by number of votes received.
        For example, if candidate 2 > candidate 1: [2, 1, 0]

    Returns
    -------
    winner: str
        Returns the name of the winning candidate
    '''
    try:
        draw_checker(list_of_votes, max_pos)

    except DrawException:
        #print("There is a draw")
        #print(list_of_votes)
        winner = "Draw"
    except ZeroException:
        #print("There is a zero")
        #print(list_of_votes)
        winner = "Zero"
    except NoDrawException:
        # In case the 0th cand has 0 list_of_votes
        winner_pos = position[max_pos]
        winner = CAND_NAMES[winner_pos]

    finally:
        return winner
##


def counter(system_list): ##
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
       Returns the name of the winning candidate. Note that it calls the
       winner_calc function and returns its output.
    '''
    try:
        counts = np.bincount(system_list)
        position = np.nonzero(counts)[0]
        list_of_votes = counts[position]
        max_pos = np.argmax(list_of_votes)
    # When there is no winner/approved
    # Error: "Attempt to get argmax of an empty sequence"
    except ValueError:
        winner = "None"
        return winner
    # winner_calc() is called only if there is a winner
    return winner_calc(list_of_votes, max_pos, position)
##
# *******************************************************************


# BALLOT GENERATOR FUNCTIONS
# ===================================================================
def fptp(dist_list): ##
    fptp_votes = np.argmin(dist_list, axis=1)
    f_winner = counter(fptp_votes)
    return f_winner
##


def approval(dist_list): ##
    APPROVAL_RADIUS = 2
    approved = np.array(np.where(dist_list <= APPROVAL_RADIUS))
    approval_list = approved[1]
    a_winner = counter(approval_list)
    return a_winner
##


def borda(d_sorted): ##
    borda_list = np.array(
        [
            np.transpose(np.nonzero(d_sorted == 0))[:, 1],
            np.transpose(np.nonzero(d_sorted == 1))[:, 1],
            np.transpose(np.nonzero(d_sorted == 2))[:, 1],
        ]
    )  # Equivalent to np.argwhere but slightly faster
    borda_sum = np.sum(borda_list, axis=1)
    borda_winner_pos = np.argmin(borda_sum)
    b_winner = CAND_NAMES[borda_winner_pos]
    return b_winner
##


def score(dist_list): ##
    # radius = [0.5, 1, 2, 3]
    # score = [10, 8, 7, 5, 0]
    # Actually makes a new array not replace
    score_list = np.zeros(dist_list.shape)
    np.place(score_list, np.logical_and(dist_list >= 2, dist_list <= 3), [5])
    np.place(score_list, np.logical_and(dist_list >= 1, dist_list <= 2), [7])
    np.place(score_list, np.logical_and(dist_list >= 0.5, dist_list <= 1), [8])
    np.place(score_list, dist_list <= 0.5, [10])

    score_sum = np.einsum('ij->j', score_list)  # Sum all columns
    score_winner_pos = np.argmax(score_sum)
    #print(score_list, score_sum)
    s_winner = winner_calc(score_sum, score_winner_pos, [0, 1, 2])
    return s_winner
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


# RUN ELECTION
N_VOTER_IN_GROUP = 1000
STDEV = 1

NUM_OF_ELECTIONS = 100
result = []

with tqdm(total=NUM_OF_ELECTIONS) as pbar:
    loop_number = 0

    while loop_number < NUM_OF_ELECTIONS: ##
        result.append(
            election(
                np.random.normal(0, 1),
                np.random.normal(0, 1),
                N_VOTER_IN_GROUP,
                STDEV
            )
        )
        pbar.update(1)
        loop_number += 1
    ##
v_x, v_y, fptp_winner, approval_winner, borda_winner, score_winner = zip(*result)
