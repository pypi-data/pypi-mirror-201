import numpy as np


def read_multi_hist(FileName: str, SpeciesList: list):
    """
    Read a multi-species histogram from a file and return a list of time steps
    and species counts.

    Parameters
    ----------
    FileName : str
        The name of the input file to read.
    SpeciesList : list
        A list of species names corresponding to the columns in the input file.

    Returns
    -------
    hist_list : List
        A list of time steps and species counts. Each element of the list is a
        NumPy array with shape (N, M+1), where N is the number of time steps and
        M is the number of species in SpeciesList. The first column contains the
        time step and the remaining columns contain the counts for each species.

    Raises
    ------
    ValueError
        If any of the species names in the input file are not found in SpeciesList.

    Examples
    --------
    >>> SpeciesList = ['A', 'B', 'C', 'D']
    >>> read_multi_hist('histogram_complexes_time.dat', SpeciesList)

    Notes
    -----
    The input file must have the following format:

    Time (s): <time>
    <complex_count><tab><species 1>: <num_of_species_1_in_complex> . <species 2>: <num_of_species_2_in_complex> . ...
    <complex_count><tab><species 1>: <num_of_species_1_in_complex> . <species 2>: <num_of_species_2_in_complex> . ...
    ...

    where <time> is the time step in seconds and <count> is the number of counts
    for each species at that time step. Each line after the first should contain
    one time step and its corresponding species counts, with species counts
    separated by periods.
    """
    speciesListArray = np.array(
        SpeciesList)  # Convert SpeciesList to a NumPy array
    histogramList = []  # Initialize empty list to store histograms
    # Initialize empty list to store complex counts for each time step
    timeStepComplexCounts = []

    # Create dictionary to store species indices
    speciesIndexDict = {speciesName: index for index, speciesName in enumerate(speciesListArray)}

    # Open file and read line-by-line
    with open(FileName, 'r') as file:
        for line in file:
            # Check if line contains time information
            if line.startswith('Time (s):'):
                time = float(line.split()[-1])   # Extract time value from line
                # Start new time step with current time value
                timeStepComplexCounts = [time]
            else:   # Line contains complex count information
                # Extract count and complex information
                count, complexInfoStr = line.strip().split('\t')
                # Split complex information into individual items
                complexItems = complexInfoStr.rstrip('.').split('. ')
                # Initialize array to store complex counts
                complexCounts = np.zeros(len(speciesListArray) + 1, dtype=int)
                for item in complexItems:
                    # Extract species name and count from complex information
                    speciesName, numStr = item.split(': ')
                    num = int(numStr)
                    # Get index of species from dictionary
                    index = speciesIndexDict[speciesName]
                    # Increment count for species in complexCounts
                    complexCounts[index] += num
                # Add total count to last element of complexCounts
                complexCounts[-1] += int(count)
                # Add complexCounts to current time step
                timeStepComplexCounts.append(complexCounts)
            # Append final time step to histogram list
            histogramList.append(timeStepComplexCounts)

    return histogramList   # Return list of histograms for each time step


