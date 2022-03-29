# simulation
# query.txt = the first column will have the index with respect to the unobserved.csv
# run it on virtual harfdware///.... outputs to txt  - "query.txt" will have index values of the unobserved.csv and "qpcrOutput.CSV" ct
# update(input:"trueCt.txt") - update & save observed.csv unobserved.csv
# uncertainty (observed.csv unobserved.csv , batch#) --> batch 3 parameter set (samples) for us to "query.txt"

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

#drop unused feature (f_seq, b_seq, T, start, stop)
#return preprossed dataframe
def preprocess(df):
    pass



def update_observed_file(observed_file, unobserved_file, trueCT_filename):
    pass

def update_unobserved_file(unobserved_filename, trueCT_filename):
    # query.txt = the first column will have the index with respect to the unobserved.csv

    unobserved = pd.read_csv(unobserved_filename)
    unobserved.drop(labels = query_index, axis = 0, inplace = True)
    unobserved.to_csv(unobserved_filename, index = False)



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
    return most_uncertain

def write_query_file(output_filename, observed_file, unobserved_file, batch_size):
    #  batch 3 parameter set (samples) for us to "query.txt"
    query_index = get_query_index(observed_file, unobserved_file, batch_size)
    unobserved = pd.read_csv(unobserved_file)
    toWrite = unobserved.iloc[query_index, :].to_csv(index = True)
    with open(output_filename, "w") as f:
        f.write(toWrite)
        f.close()
    return toWrite



