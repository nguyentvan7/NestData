import pandas as pd
import matplotlib.pyplot as plt

startDate = '2024-07-01'
endDate = '2024-07-02'

df = pd.read_csv('cycles.csv')
df.columns = ['Timestamp', 'State', 'Duration']
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='ISO8601').dt.tz_convert('US/Pacific')
df['Duration'] = pd.to_timedelta(df['Duration'])
mask = (df['Timestamp'] > startDate) & (df['Timestamp'] < endDate)
df = df.loc[mask]
df = df.set_index('Timestamp')

averageOn = df.query('State == 0').loc[:, 'Duration'].mean()
averageOff = df.query('State == 1').loc[:, 'Duration'].mean()
numCyclesOn = len(df.query('State == 0').index)
numCyclesOff = len(df.query('State == 1').index)
totalOn = df.query('State == 0').loc[:, 'Duration'].sum()
totalOff = df.query('State == 1').loc[:, 'Duration'].sum()

text = '\n'.join((
    'averageOn = ' + str(averageOn),
    'averageOff = ' + str(averageOff),
    'numCyclesOn = ' + str(numCyclesOn),
    'numCyclesOff = ' + str(numCyclesOff),
    'totalOn = ' + str(totalOn),
    'totalOff = ' + str(totalOff),
))

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig, ax = plt.subplots()
ax.text(0.05, 1.1, text, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
ax.step(df.index, df['State'])

plt.show()