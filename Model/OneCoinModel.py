import random
from math import comb, ceil
from functools import lru_cache
from fractions import Fraction
from tqdm import tqdm 

PROB = Fraction(1, 3) 

class OneCoinModel: 
    '''
    Simulation model for Game 1. 
    '''
    def __init__(self, max_I1, max_I2, max_d): 
        self.max_I = max(max_I1, max_I2) 
        self.max_d = max_d
        self.dict_D = {} 
        self._precompute_D()

    def _precompute_D(self):
        for m in tqdm(
            range(1, self.max_I),
            desc="Precomputing D(m,n)"
        ):
            for n in range(1, self.max_I):
                self.dict_D[(m, n)] = self._D(m, n)


    def simulate_tie_prob(self, k: int, r = 1, n_trials: int = 100000) -> float:
        tie_count = 0
        for _ in range(n_trials):
            a = b = k
            while True:
                a_toss, b_toss = random.randint(0, 1), random.randint(0, 1)
                a -= a_toss * r 
                b -= b_toss * r 
                if a <= 0 and b <= 0: # if both players reach (0, 0), then it is considered a tie
                    tie_count += 1
                    break
                elif a <= 0 or b <= 0: # if only one player reaches (0, 0) or below, then it is no longer a tie
                    break
        return tie_count / n_trials        
    

    def tie_prob_by_combinations(self, k, r=1):
        t = ceil(k / r)
        total = Fraction(0, 1)
        for n in range(t):
            c1 = comb(2 * t - n - 2, n)
            c2 = comb(2 * t - 2 * n - 2, t - n - 1)
            power = 2 * t - n - 1
            term = Fraction(c1 * c2, 3**power)  
            total += term
        return total


    @lru_cache(None)
    def tie_prob_by_recurrence(self, m, n, d=1):
        if m <= 0 and n <= 0:
            return Fraction(1, 1)
        if (m <= 0 and n > 0) or (n <= 0 and m > 0):
            return Fraction(0, 1)
        return (
            self.tie_prob_by_recurrence(m - d, n, d) +
            self.tie_prob_by_recurrence(m, n - d, d) +
            self.tie_prob_by_recurrence(m - d, n - d, d)
        ) / 3
    
    @lru_cache(None)
    def _multinomial(self, a, b, c):
        return comb(a + b + c, a) * comb(b + c, b)

    def _D(self, m, n, prob = PROB):
        total = Fraction(0, 1)
        for ell in range(min(m, n) + 1):
            coeff = self._multinomial(m - ell, n - ell, ell)
            total += coeff * prob ** (m + n - ell)
        return total

    def _coeff_B(self, I1, I2, d): 
        result = Fraction(0) 
        if I1 % d or I2 % d: 
            return result 
        result += self._D(I1 // d, I2 // d) 
        return result

    def tie_prob_by_gf(self, m, n, d, prob = PROB):
        total = Fraction(0)
        alpha_steps = (d, )
        beta_steps  = (d,)
        step_pairs = [(x, y) for x in alpha_steps for y in beta_steps]
        for a, b in step_pairs:
            for M in range(1, min(a, m) + 1):
                for N in range(1, min(b, n) + 1):
                    total += self._coeff_B(m - M, n - N, d)
        return prob * total