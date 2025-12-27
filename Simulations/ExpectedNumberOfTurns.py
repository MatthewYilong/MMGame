import random


def simulate_game(I1, I2): 
    turns = 0
    while I1 > 0 and I2 > 0: 
        turns += 1
        coin_flip1 = random.randint(0, 1)
        coin_flip2 = random.randint(0, 1) 
        I1 -= coin_flip1
        I2 -= coin_flip2
    return turns

def estimate_expected_turns(I1, I2, num_simulations): 
    total_turns = 0
    for _ in range(num_simulations): 
        total_turns += simulate_game(I1, I2)
    expected_turns = total_turns / num_simulations 
    return expected_turns


def simulate_mm_game():
    initial_coins = [(10, 10), (20, 20), (50, 50)] 
    num_simulations = 10000
    print("Expected Number of Turns:") 
    for I1, I2 in initial_coins:
        expected_turns = estimate_expected_turns(I1, I2, num_simulations) 
        print(f"Players with {I1} and {I2} coins: {expected_turns:.2f} turns")

 
 