import numpy as np

array = np.array([1,2,3,4,5])

r = np.concatenate([[0],array,[77]])
print(r)