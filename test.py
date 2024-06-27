import numpy as np
import pandas as pd

test = np.arange(13, dtype=int)
highest_hand = np.zeros(13, dtype=int)

print(np.append(test, highest_hand, axis=0))
