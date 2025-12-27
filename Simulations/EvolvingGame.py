import numpy as np
import matplotlib.pyplot as plt

def calculate_tie_probability(n, lambda_val,num_simulations): 
    num_ties = 0
    for _ in range(num_simulations):
        m_A, m_B = n, n
    while m_A > 0 and m_B > 0:
        P_heads_A = 1 - np.exp(-lambda_val * (n - m_A + 1)) 
        P_heads_B = 1 - np.exp(-lambda_val * (n - m_B + 1)) 
        if np.random.rand() < P_heads_A:
            m_A -= 1
        if np.random.rand() < P_heads_B:
            m_B -= 1
        if m_A == 0 and m_B == 0:
            num_ties += 1
        return num_ties / num_simulations


def probability_vs_lambda(n, lambda_values, num_simulations): 
    tie_probabilities = []
    for lambda_val in lambda_values:
        tie_probabilities.append(calculate_tie_probability(n, lambda_val,num_simulations))
    plt.figure()
    plt.plot(lambda_values, tie_probabilities, "o-", label="Probability of Tie") 
    plt.xlabel("Lambda Value")
    plt.ylabel("Probability of Tie")
    plt.title("Probability of Tie vs Lambda Value")
    plt.legend()
    plt.grid(True)
    plt.show()
 
n = 200
lambda_values = np.linspace(0.1, 5, 30) 
num_simulations = 100000
probability_vs_lambda(n, lambda_values, num_simulations)
