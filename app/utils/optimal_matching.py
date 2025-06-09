import numpy as np
from scipy.optimize import linear_sum_assignment

def optimize_matching_globally(mentees, mentors):
    """
    Optimize the matching between mentees and mentors using the Hungarian algorithm.
    
    Args:
        mentees (list): List of mentee objects.
        mentors (list): List of mentor objects.
    
    Returns:
        list: List of tuples containing matched pairs (mentee, mentor).
    """
    num_mentees = len(mentees)
    num_mentors = len(mentors)

    # Create a cost matrix where each entry is the negative matching score
    cost_matrix = np.zeros((num_mentees, num_mentors))

    for i, mentee in enumerate(mentees):
        for j, mentor in enumerate(mentors):
            cost_matrix[i, j] = -calculateMatchingRate(mentee, mentor)

    # Use the Hungarian algorithm to find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Create matched pairs
    matches = [(mentees[row], mentors[col]) for row, col in zip(row_ind, col_ind)]

    return matches
