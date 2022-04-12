'''
Pick 3 random points as first query
Write those indices to query_filename

Read entire dataset from unobserved_filename as unobserved
Pick 3 most uncertain to query
Drop indices from unobserved -> update unobserved


'''

import AL
import init

def main():
    
    # init.init("simDataGC.txt", 3, "query.csv", True)

    AL.write_qPCR_output("qPCR_output.txt")

    AL.update_observed_file("observed.txt", "query.csv", False)
    AL.update_unobserved_file("unobserved.txt", "query.csv")
    AL.write_query_file("query.csv", "observed.txt", "unobserved.txt", 3, False)


if __name__ == "__main__":
    main()