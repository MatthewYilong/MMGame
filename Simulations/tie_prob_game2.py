import csv
from itertools import product
from tqdm import tqdm
from Code.Model.PartialTwoCoinModel import PartialTwoCoinModel

OUTFILE = "/Users/matthewwu/desktop/research/Data/tie_prob_game2.csv"

MAX_I = 100
MAX_d = 20

model = PartialTwoCoinModel(
    max_I1=MAX_I,
    max_I2=MAX_I,
    max_d1=MAX_d,
    max_d2=MAX_d
)

I1_range = range(1, MAX_I + 1)
I2_range = range(1, MAX_I + 1)
d1_range = range(1, MAX_d + 1)
d2_range = range(1, MAX_d + 1)

TOTAL = MAX_I * MAX_I * MAX_d * MAX_d

with open(OUTFILE, "w", newline="") as f:
    writer = csv.writer(f)

    # header
    writer.writerow(["I1", "I2", "d1", "d2", "gf", "rec", "equal"])

    for I1, I2, d1, d2 in tqdm(
        product(I1_range, I2_range, d1_range, d2_range),
        total=TOTAL,
        desc="Computing tie probabilities"
    ):
        gf  = model.tie_prob_by_gf(I1, I2, d1, d2)
        rec = model.tie_prob_by_recurrence(I1, I2, d1, d2)

        writer.writerow([
            I1,
            I2,
            d1,
            d2,
            str(gf),               
            str(rec),
            gf == rec              
        ])
