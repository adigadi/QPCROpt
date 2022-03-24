# simulation
# run it on virtual harfdware///.... outputs to txt  - "trueCt.txt" will have index values of the unobserved.csv and ct
# update(input:"trueCt.txt") - update & save observed.csv unobserved.csv
# uncertainty (observed.csv unobserved.csv , batch#) --> batch 3 parameter set (samples) for us to "query.txt"

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

#drop unused feature (f_seq, b_seq, T, start, stop)
#return preprossed dataframe
def preprocess(df):
    pass

#read observed.csv
# return the uncertainty of each unobserved data
def get_query_index(observed_file, unobserved_file, batch_size):
    most_uncertain = []
    unobserved = pd.read_csv(unobserved_file)
    observed = pd.read_csv(observed_file)
    X, y = observed[["fwdGC", "revGC"]], observed["Ct"]
    reg = RandomForestRegressor(n_estimators=3,random_state=0)
    reg.fit(X,y ) #observed
    # find the most uncertain
    outputs = []
    for estimator in reg.estimators_:
        outputs.append(estimator.predict(unobserved[["fwdGC", "revGC"]])) #unobserved
    stds = np.std(outputs, axis=0)
    for i in range(batch_size):
        max_index = int(np.argmax(stds))
        most_uncertain.append(max_index)
        stds[max_index] = -1
    # probas = stds/sum(stds) #makes them sum to 1
    # numerical_selected_indices = np.random.choice(
    #         range(len(probas)),
    #         size=batch_size,
    #         replace=False,
    #         p=probas)
    # selected_indices = [available_indices[i] for i 
    #                 in numerical_selected_indices]
     # select the one with greatest error or highest standard deviation
    return 

# return the top M most uncertainty combinations index
# M: batch size
def get_query_index(df):
    pass

def write_query_file(df, filename, query_index):
    pass

def update_observed_file(df, query_index):
    pass

def update_unobserved_file(df, query_index):
    pass

def

