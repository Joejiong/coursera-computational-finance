import csv
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

simulation_rounds = 100000
simulation = {}
with open('..\\resources\\week3\\senate.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        state = row['State']
        mean = float(row['Republican Margin'])
        std_dev = float(row['Margin of error'])
        simulation[state] = np.random.normal(loc=mean, scale=std_dev, size=simulation_rounds)

round_results = []
for i in range(simulation_rounds):
    state_wins = 0
    # for each round draw poll for each state
    for poll in simulation.values():
        if poll[i] > 0:
            state_wins += 1
    round_results.append(state_wins)

senate_wins = filter(lambda wins: wins >= 21, round_results)
x = np.array(round_results)
prob_win = 1 - norm(x.mean(), x.std()).cdf(21)
print prob_win

plt.hist(round_results, bins=(np.amax(round_results) - np.amin(round_results)), normed=True)
plt.title('Election Results')
plt.xlabel('Margin')
plt.ylabel('Probability')
plt.show()





