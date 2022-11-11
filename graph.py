from matplotlib import pyplot as plt
from math import log

def plot_sequence(arr):
    xs = [1]
    ys = [1]
    x = y = 1
    bucket = 1
    for k in arr:
        bucket *= k
        for _ in range(bucket):
            x += 1
            y -= log(bucket)
            xs.append(x)
            ys.append(y)
    plt.plot(xs, ys)

plot_sequence([2, 2, 2, 2, 2, 2, 2, 2, 2])
plot_sequence([3, 2, 2, 2, 2, 2, 2, 2])
plot_sequence([5, 2, 2, 2, 2, 2, 2])
plt.show()