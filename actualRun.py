import AL


def main():
    
    AL.write_qPCR_output("qPCR_output.txt") # read qPCR spreadsheet and write to txt file

    AL.update_observed_file("observed.txt", "query.csv", "qPCR_output.txt", False) # read queries, add CT values, and add queries to observed file
    AL.update_unobserved_file("unobserved.txt", "query.csv") # remove recently updated rows from unobserved file
    AL.write_query_file("query.csv", "observed.txt", "unobserved.txt", 12, False) # update model and pick new queries


if __name__ == "__main__":
    main()