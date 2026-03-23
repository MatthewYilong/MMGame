import random 
import numpy as np 
from tqdm import tqdm
import csv

OUTFILE = "PUT YOUR FILE PATH HERE"

N, lambda_values = 400, np.linspace(0.1, 5, 50) 
N_TRIALS = 100_000

def calculate_tie_probability(n, lambda_val,n_trials = N_TRIALS): 
    '''
    Given n starting number of MMs for both players and a particular lambda.  
    '''
    num_ties = 0
    for _ in range(n_trials):
        m_A, m_B = n, n
        while m_A > 0 and m_B > 0:
            if np.random.rand() < 1 - np.exp(-lambda_val * (n - m_A + 1)):
                m_A -= 1
            if np.random.rand() < 1 - np.exp(-lambda_val * (n - m_B + 1)) :
                m_B -= 1
        if m_A == 0 and m_B == 0:
            num_ties += 1
    return num_ties / n_trials


rows = [] 

with open(OUTFILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Lambda", "n", "tie_prob"])
    for lambda_value in tqdm(lambda_values):
        for n in tqdm(range(1, N+1), leave=False):
            tie_prob = calculate_tie_probability(n, lambda_value)
            writer.writerow([lambda_value, 
                             n, 
                             tie_prob])

 