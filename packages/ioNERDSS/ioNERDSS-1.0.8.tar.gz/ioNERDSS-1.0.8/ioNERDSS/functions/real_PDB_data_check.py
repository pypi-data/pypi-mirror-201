def real_PDB_data_check(data):
    if len(data) != 12:
        if len(data[2]) > 4:
            return -1  # Amino acid name stick with info before
    else:
        if len(data[3]) == 3:
            return 1  # True data
        else:
            return -2  # Wrong amino acid name


# This function will go over every atom between two chains to determine whether they are interacting (distance smaller
# than 3.0A)
# remember to import math package when use the function
# Input variables:
# return variables: a tuple includes
