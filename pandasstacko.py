import pandas as pd

rawData = {'t': 1525019820000, 'T': 1525019879999, 'o': '0.07282300', 'c': '0.07290700', 'h': '0.07293300', 'l': '0.07279800', 'v': '48.57300000'}

df = pd.DataFrame([rawData])
df['t'] = pd.to_datetime(df['t'], unit='ms')
df['T'] = pd.to_datetime(df['T'], unit='ms')
print(df.to_string(justify='center', columns=['t','T','o','c','h','l','v'], header=['from','to','open','close','high','low','vol'],  formatters={'t': lambda x: x.strftime("%H:%M:%S"), 'T': lambda x: x.strftime("%H:%M:%S")}))
