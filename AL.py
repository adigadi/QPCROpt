# simulation
# query.txt = the first column will have the index with respect to the unobserved.csv
# run it on virtual harfdware///.... outputs to txt  - "query.txt" will have index values of the unobserved.csv and "qpcrOutput.CSV" ct
# update(input:"trueCt.txt") - update & save observed.csv unobserved.csv
# uncertainty (observed.csv unobserved.csv , batch#) --> batch 3 parameter set (samples) for us to "query.txt"
from email.charset import QP
import os
import fnmatch
import numpy as np
import random
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

#checked
def find_qPCR_file():
    for filename in os.listdir('.'):
        if fnmatch.fnmatch(filename, '*Results*.xls'):
            return filename

#checked
def read_qPCR_file(qPCR_filename):
    raw_df = pd.read_excel(qPCR_filename)
    raw_df.columns = raw_df.iloc[39,:].values.flatten().tolist()
    df = raw_df.iloc[40:,:]
    qPCR_df = df[['Well Position', 'CT', 'Ct Mean']].copy()
    qPCR_df.columns = ['well', 'ct', 'mean_ct']
    return qPCR_df

#checked
def write_qPCR_output(filename):
    qPCR_filename = find_qPCR_file() # excel spreadsheet
    qPCR_df = read_qPCR_file(qPCR_filename)
    qPCR_df.to_csv(filename, index=False)
    
def setTrueCt(query_df, qPCR_df):
    trueCT_values = qPCR_df["mean_ct"]
    query_df["mean_ct"] = trueCT_values
    query_df = query_df.dropna()
    return query_df

def setSimCT(simDataDir, queryDir):
    simDf = pd.read_csv(simDataDir)
    queryDf = pd.read_csv(queryDir)
    queryIdx = queryDf["idx"].values
    print("printing queryIdx")
    print(queryIdx)
    # ct = []
    # for i in queryIdx:
    #     ct.append(simDf[simDf["idx"] == i]["Ct"])

    print("simDf")
    print(simDf)
    queryDf["Ct"] = simDf.iloc[queryIdx]["Ct"].values
    print("queryDf")
    print(queryDf)
    return queryDf

#query file: index, content
#observed: dataframe
#qPCROutput: not Known
def update_observed_file(observed_filename, query_filename, qPCR_filename, first_run, sim, simDataDir):
    if first_run == True:
        observed = pd.DataFrame()
    else:
        observed = pd.read_csv(observed_filename)
    query = pd.read_csv(query_filename)
    qPCR = pd.read_csv(qPCR_filename)
    if not sim:
        query_ct = setTrueCt(query, qPCR)
    else:
        query_ct = setSimCT(simDataDir, query_filename)
    print("before appending")
    print(query_ct)
    print(observed)
    observed = observed.append(query_ct, ignore_index=True, sort = False)
    print("after appending")
    print(observed)
    observed.to_csv(observed_filename, index = False)

def update_unobserved_file(unobserved_filename, query_filename):
    # query.txt = the first column will have the index with respect to the unobserved.csv
    unobserved = pd.read_csv(unobserved_filename)
    query_index = pd.read_csv(query_filename)["idx"].to_numpy()
    print(query_index)
    label = unobserved[unobserved.idx.isin(query_index)].index
    print("update_unobs label")
    print(label)
    unobserved.drop(labels = label, axis = 0, inplace = True)
    unobserved.to_csv(unobserved_filename, index = False)

#read observed.csv
# return the uncertainty of each unobserved data
def get_query_index(observed_file, unobserved_file, batch_size, first_run):
    
    most_uncertain = []
    unobserved = pd.read_csv(unobserved_file)
    
    
    if first_run == True: 
        #random selected seeds
        most_uncertain = random.sample(list(range(len(unobserved))), batch_size)
    
    else: 
        #uncertainty sampling
        observed = pd.read_csv(observed_file)
        X, y = observed[["forward GC", "reverse GC", "Mg Conc", "dist"]], observed["mean_ct"]
        reg = RandomForestRegressor(n_estimators=3,random_state=0)
        reg.fit(X,y) #observed
        # find the most uncertain
        outputs = []
        for estimator in reg.estimators_:
            outputs.append(estimator.predict(unobserved[["forward GC", "reverse GC", "Mg Conc","dist"]])) #unobserved
        stds = np.std(outputs, axis=0)
        for i in range(batch_size):
            max_index = int(np.argmax(stds))
            most_uncertain.append(max_index)
            stds[max_index] = -1
            
    return most_uncertain

#first_run: boolean var -- True if write initial seeds as query, False if write selected batch by uncertainty sampling
def write_query_file(query_filename, observed_file, unobserved_file, batch_size, first_run):
    #  batch 3 parameter set (samples) for us to "query.csv" 
    query_index = get_query_index(observed_file, unobserved_file, batch_size, first_run)
    print("query_idx")
    print(query_index)
    unobserved = pd.read_csv(unobserved_file)
    print("unobserved")
    print(unobserved)
    print("iloc thingy")
    print(unobserved.iloc[query_index, :])
    unobserved.iloc[query_index, :].to_csv(query_filename,index = False)

