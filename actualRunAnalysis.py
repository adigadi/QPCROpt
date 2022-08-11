# %%
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as mse
from matplotlib import pyplot as plt

# %%
"""
Read in files
"""
trainingData = []
for i in range(1,4):
    trainingData.append(pd.read_csv(f"observedRound{i}.txt"))
# %%
testData = pd.read_csv("observedRound4OnlyAkaTestData.txt")
# %%
"""
training model
"""
score = []
for i in range(len(trainingData)):
    X, y = trainingData[i][["forward GC", "reverse GC", "Mg Conc", "dist"]], trainingData[i]["mean_ct"]
    reg = RandomForestRegressor(n_estimators=3,random_state=0)
    reg.fit(X,y)
    score.append(mse(reg.predict(testData[["forward GC", "reverse GC", "Mg Conc", "dist"]]),testData["mean_ct"]))
# %%
"""
plotting
"""
plt.plot([len(trainingData[i]) for i in range(len(trainingData))], score)
plt.xlabel("number of instances queried")
plt.ylabel("mean squared error")
plt.show()
# %%
"""
predict all
"""
allInst = pd.read_csv("unobserved.txt")
yHat = reg.predict(allInst[["forward GC", "reverse GC", "Mg Conc", "dist"]])
# %%
yHatArgsort = np.argsort(yHat)
allInst.iloc[yHatArgsort[0:5]]
# %%
