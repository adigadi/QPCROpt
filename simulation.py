import AL
import pandas as pd


def main():
    
    AL.write_qPCR_output("qPCR_output.txt") # read qPCR spreadsheet and write to txt file

    AL.update_observed_file("obsSim.txt", "query.csv", "qPCR_output.txt", False, True, "simDataGC.txt") # read queries, add CT values, and add queries to observed file
    AL.update_unobserved_file("unobsSim.txt", "query.csv") # remove recently updated rows from unobserved file
    AL.write_query_file("query.csv", "obsSim.txt", "unobsSim.txt", 3, False) # update model and pick new queries


if __name__ == "__main__":
    main()