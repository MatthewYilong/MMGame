import csv
from itertools import product
from tqdm import tqdm
from Code.Model.OneCoinModel import OneCoinModel

OUTFILE = "/Users/matthewwu/desktop/research/Data/tie_prob_game1.csv"

MAX_I = 100
MAX_d = 20

model = OneCoinModel(
    max_I1=MAX_I,
    max_I2=MAX_I,
    max_d=MAX_d)

I1_range = range(1, MAX_I + 1)
I2_range = range(1, MAX_I + 1)
d_range = range(1, MAX_d + 1)

TOTAL = MAX_I * MAX_I * MAX_d

with open(OUTFILE, "w", newline="") as f:
    writer = csv.writer(f)

    # header
    writer.writerow(["I1", "I2", "d1", "gf", "rec", "equal"])

    for I1, I2, d in tqdm(
        product(I1_range, I2_range, d_range),
        total=TOTAL,
        desc="Computing tie probabilities"
    ):
        gf  = model.tie_prob_by_gf(I1, I2, d)
        rec = model.tie_prob_by_recurrence(I1, I2, d)

        writer.writerow([
            I1,
            I2,
            d,
            str(gf),              
            str(rec),
            gf == rec             
        ])
