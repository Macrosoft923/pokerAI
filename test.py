import numpy as np

np.random.seed(123)
x = np.random.randint(9, size=(3, 3))

print(x)
print(x.item(3))

y = np.random.randint(10, size=(1, 10))

print(y)
print(y.item(-1))
