import pandas as pd
"""
input:  dataFileDir: the filename of all simulation data (simulation) or of unobserved (actual)
        batchSize: size of each query (3 in simulation; 12 in actual)
        output_filename: equivalent to query.csv
        sim: whether it is simulation
Randomly selects batchSize number of unlabeled samples (drop Ct)
Writes to output_filename
returns: the queries as a dataframe
"""


def main():

    init("simDataGC.txt", 3, "query.csv", True) # pick 3 initial queries


def init(dataFileDir, batchSize, output_filename, sim):
    df = pd.read_csv(dataFileDir)
    # print(df)
    init = df.sample(batchSize)
    # print(init)
    init["idx"] = init.index
    if sim:
        init.drop("Ct", axis = 1).to_csv(output_filename,index = False)
    else:
        init.to_csv(output_filename,index = False)
    return init

if __name__ == "__main__":
    main()
