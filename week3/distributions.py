import numpy as np
import matplotlib.pyplot as plt

mean = 0.0
std_dev = 4.0
s = np.random.normal(loc=mean, scale=std_dev, size=10000)
count, bins, ignored = plt.hist(s, 30, normed=True)
plt.plot(bins, 1 / (std_dev * np.sqrt(2 * np.pi)) *
         np.exp(- (bins - mean) ** 2 / (2 * std_dev ** 2)),
         linewidth=2, color='r')
plt.show()