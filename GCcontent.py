# %%
from gc import collect
from itertools import count
import pandas as pd
import collections

df = pd.read_csv('simulationData.txt')
df.head()
# %%
fwd = df['Forward'].tolist()
rev = df['reverse'].tolist()

gc_fwd = []
gc_rev = []

for primer in fwd:
    counts = collections.Counter(primer)
    print(counts)
    gc_count = counts['G'] + counts['C']
    gc_content = gc_count / len(primer)
    gc_fwd.append(gc_content)

for primer in rev:
    counts = collections.Counter(primer)
    gc_count = counts['G'] + counts['C']
    gc_content = gc_count / len(primer)
    gc_rev.append(gc_content)
# %%
df['fwdGC'] = gc_fwd
df['revGC'] = gc_rev
df.head()
# %%
