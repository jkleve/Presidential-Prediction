import numpy as np
import matplotlib.pyplot as plt

# feature 1
f1 = [69.8, 80.91, 69.72, 80.39]
bins = np.arange(65,85,1)

def gen_histogram(accuracies, bins):
    mu, sigma = 100, 15
    hist, bins = np.histogram(accuracies, bins=bins)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

if __name__ == "__main__":
    gen_histogram(f1, bins)
