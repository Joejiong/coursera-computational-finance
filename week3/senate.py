import csv
import numpy as np

samples = {}
with open('..\\resources\\week3\\senate.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        state = row['State']
        mean = float(row['Republican Margin'])
        std_dev = float(row['Margin of error'])
        samples[state] = np.random.normal(loc=mean, scale=std_dev, size=10)

