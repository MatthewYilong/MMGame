import random
from math import comb 
from fractions import Fraction
from functools import lru_cache
from tqdm import tqdm 

PROB = Fraction(1, 15) 

class TwoCoinModel: 
    '''
    Simulation model for Game 3. 
    '''
    def __init__(self, max_I1, max_I2, max_d1, max_d2):
        self.dict_nonnegative_sols = {} 
        self.dict_D = {} 
        self.dict_coeff_B = {} 
        self.max_I = max(max_I1, max_I2) + 1
        self.max_d1, self.max_d2 = max_d1, max_d2 
        self._precompute_nonnegative_solutions()
        self._precompute_D()

    def _precompute_nonnegative_solutions(self):
        for I in tqdm(
            range(1, self.max_I),
            desc="Precomputing nonnegative solutions (I)"
        ):
            for d1 in range(1, self.max_d1 + 1):
                for d2 in range(1, self.max_d2 + 1):
                    self.dict_nonnegative_sols[(d1, d2, I)] = \
                        self._nonnegative_solutions(d1, d2, I)
                    
    def _precompute_D(self):
        for m in tqdm(
            range(1, self.max_I),
            desc="Precomputing D(m,n)"
        ):
            for n in range(1, self.max_I):
                self.dict_D[(m, n)] = self._D(m, n)

    def simulate_tie_probability(self, m: int, n,  d1 = 1, d2 = 1, n_trials: int = 10000000) -> float:
        tie_count = 0
        for _ in range(n_trials):
            a = m 
            b = n 
            while True:
                a_toss_1, a_toss_2 = random.randint(0, 1), random.randint(0, 1)
                b_toss_1, b_toss_2 = random.randint(0, 1), random.randint(0, 1)
                a -= a_toss_1 * d1 + a_toss_2 * d2
                b -= b_toss_1 * d1 + b_toss_2 * d2            
                if a <= 0 and b <= 0: 
                    tie_count += 1
                    break
                elif a <= 0 or b <= 0: 
                    break
        return tie_count / n_trials
    
    @lru_cache(None)
    def tie_prob_by_recurrence(self, m, n, d1=1, d2=1):
        if m <= 0 and n <= 0:
            return Fraction(1)
        if m <= 0 < n or n <= 0 < m:
            return Fraction(0)
        return Fraction(1, 15) * (
            self.tie_prob_by_recurrence(m = m - d1 - d2, n = n - d1 - d2, d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d1 - d2, n = n - d1     , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d1 - d2, n = n - d2     , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d1 - d2, n = n          , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d1     , n = n - d1 - d2, d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d1     , n = n - d1     , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d1     , n = n - d2     , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d1     , n = n          , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d2     , n = n - d1 - d2, d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d2     , n = n - d1     , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d2     , n = n - d2     , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m - d2     , n = n          , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m          , n = n - d1 - d2, d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m          , n = n - d1     , d1 = d1, d2 = d2) + 
            self.tie_prob_by_recurrence(m = m          , n = n - d2     , d1 = d1, d2 = d2) 
        )

    @lru_cache(None)
    def _multinomial(self, a, b, c):
        return comb(a + b + c, a) * comb(b + c, b) 
    
    def _D(self, m, n, prob = PROB):
        total = Fraction(0, 1)
        if (m,n) in self.dict_D: 
            total = self.dict_D[(m, n)]
        else: 
            for ell in range(min(m, n) + 1):
                coeff = self._multinomial(m - ell, n - ell, ell)
                total += coeff * prob ** (m + n - ell)
            self.dict_D[(m, n)] = total 
        return total
    
    def _nonnegative_solutions(self, d1, d2, I): 
        sols = []
        if (d1,d2,I) in self.dict_nonnegative_sols: 
            sols = self.dict_nonnegative_sols[(d1,d2,I)]
        else: 
            for a in range(I + 1):
                for b in range(I + 1):
                    for c in range(I + 1):
                        if (a + c)*d1 + (b + c)*d2 == I:
                            sols.append((a, b, c))
            self.dict_nonnegative_sols[(d1,d2,I)] = sols 
        return sols
    
    def _coeff_B(self, I1, I2, d1, d2): 
        result = Fraction(0) 
        for r, s, t in self._nonnegative_solutions(d1, d2, I1): 
            for i, j, k in self._nonnegative_solutions(d1, d2, I2): 
                result += self._multinomial(r,s,t) * self._multinomial(i,j,k) * self._D(r + s + t, i + j + k) 
        return result
    
    def tie_prob_by_gf(self, m, n, d1, d2, prob = PROB):
        total = Fraction(0)
        alpha_steps = (d1, d2, d1 + d2)
        beta_steps  = (d1, d2, d1 + d2)
        step_pairs = [(x, y) for x in alpha_steps for y in beta_steps]
        for a, b in step_pairs:
            for M in range(1, min(a, m) + 1):
                for N in range(1, min(b, n) + 1):
                    if (m - M, n - N, d1, d2) in self.dict_coeff_B: 
                        total += self.dict_coeff_B[(m - M, n - N, d1, d2)] 
                    else: 
                        coeff = self._coeff_B(m - M, n - N, d1, d2)
                        total += coeff
                        self.dict_coeff_B[(m - M, n - N, d1, d2)] = coeff
        return prob * total


