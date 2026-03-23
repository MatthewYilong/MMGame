# MMGame

This repository contains the source code for the paper *Generalizations of the M\&Ms Game* ([arXiv link](https://arxiv.org/abs/2502.07402)).

The codebase is organized as follows:

- The directory **`Model/`** contains the core simulation code for the three generalized games presented in Section 2 of the paper.
  - `OneCoinModel.py` simulates Game 1.
  - `PartialTwoCoinModel.py` simulates Game 2.
  - `TwoCoinModel.py` simulates Game 3.

- The directory **`Simulations/`** contains scripts for running simulations of the generalized M\&M Games over specified parameter ranges.
  - `simulate_game1.py` simulates Game 1 over the parameter range  
    $(I_1, I_2, d) \in [100] \times [100] \times [20]$.
  - `simulate_game2.py` simulates Game 2 over the parameter range  
    $(I_1, I_2, d, d_1, d_2) \in [100] \times [100] \times [20] \times [20] \times [20]$.
  - `simulate_game3.py` simulates Game 3 over the parameter range  
    $(I_1, I_2, d_1, d_2) \in [100] \times [100] \times [20] \times [20]$.
  - `EvolvingProbsMC.py` performs Monte Carlo simulations for the Evolving Coin Probabilities Game proposed in Section 3 of the paper.

The Python simulations have very minimal dependency requirements. 