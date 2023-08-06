import numpy as np
import os
import matplotlib.pyplot as plt


def multi_hist(file_name: str = 'histogram_complexes_time.dat', file_num: int = 1, start_time: float = 0, end_time: float = 0,
               target_list: list = ['all'], bin_nums: int = 10, threshold: int = 0, show_fig: bool = True, save_fig: bool = False) -> tuple:
    """
    Generate histogram of the size of target species for a multiple species system for the given species 
    and targets from the histogram_complexes_time.dat in the input file within the specified time range.

    Args:
        file_name (str): The name of the input file. Default is 'histogram_complexes_time.dat'
        file_num (int): The number of files to read. Default is 1.
        start_time (float): The start time of the time range (inclusive). Default is 0.
        end_time (float): The end time of the time range (exclusive). Default is 0. But will set to the length of the trace in the function if it is 0.
        target_list (list): The list of targets for whose number will be counted as the size of the complex. Default is all species.
        bin_nums (int, optional): The number of bins in the histogram. Default is 10.
        threshold (int, optional): The minimum value required to include a data point in the histogram. Default is 0.
        show_fig (bool, optional): Whether to display the generated figures. Default is True.
        save_fig (bool, optional): Whether to save the generated figures. Default is False.

    Returns:
        the np.arrays of normalized counts, means, and standard deviations for the histograms.
    """

    file_name_head, file_name_tail = os.path.splitext(file_name)

    # Create dictionary to store count of one size
    sizeDictList = []
     
    for i in range(1, file_num+1):
        # check if there is a folder named '1' in the current folder, if there is, set the temp_file_name to ./i/file_name, then check if ./i/file_name exited. if not exited, throw out a file not exit error.
        # else if file_num is 1, check if there is file named file_name in the current folder, if there is, set the temp_file_name to file_name; if file_num > 1, check if there is afile name file_name_head + '_' + str(i) + '.' + file_name_tail, if it is, set as the temp_file_name
        # else throw a file not found error
        temp_file_name = ""
        if os.path.isdir(str(i)):
            temp_file_name = os.path.join(str(i), file_name)
            if not os.path.isfile(temp_file_name):
                raise FileNotFoundError(f"File {temp_file_name} does not exist.")
        elif file_num == 1:
            if os.path.isfile(file_name):
                temp_file_name = file_name
            else:
                raise FileNotFoundError(f"File {file_name} does not exist.")
        else:
            temp_file_name = f"{file_name_head}_{i}.{file_name_tail}"
            if not os.path.isfile(temp_file_name):
                raise FileNotFoundError(f"File {temp_file_name} does not exist.")

        sizeDict = {}
        # Open file and read line-by-line
        with open(temp_file_name, 'r') as file:
            found_start_time = False

            for line in file:
                # Check if line contains time information
                if line.startswith('Time (s):'):
                    time = float(line.split()[-1])   # Extract time value from line
                    if time < start_time:
                        continue
                    elif time >= end_time:
                        break
                    else:
                        found_start_time = True

                else:   # Line contains complex count information
                    if found_start_time:
                        # Extract count and complex information
                        count, complexInfoStr = line.strip().split('\t')
                        count = int(count)
                        # Split complex information into individual items
                        complexItems = complexInfoStr.rstrip('.').split('. ')
                        size = 0
                        for item in complexItems:
                            # Extract species name and count from complex information
                            speciesName, numStr = item.split(': ')
                            num = int(numStr)
                            if target_list[0] == 'all' and len(target_list) == 1:
                                size += num
                            else:
                                if speciesName in target_list:
                                    size += num
                        if size > threshold:
                            if size not in sizeDict:
                                sizeDict[size] = count
                            else:
                                sizeDict[size] += count
        sizeDictList.append(sizeDict)
        
    # Combine counts of all sizes from all dictionaries
    combined_counts = {}
    for d in sizeDictList:
        for size, count in d.items():
            if size in combined_counts:
                combined_counts[size].append(count)
            else:
                combined_counts[size] = [count]

    # Calculate mean and standard deviation for each size
    mean_std = {}
    for size, counts in combined_counts.items():
        mean = np.mean(counts)
        std = np.std(counts)
        mean_std[size] = (mean, std)

    mean_std = dict(sorted(mean_std.items()))
    size_array = np.array(list(mean_std.keys()))
    mean_array = np.array([value[0] for value in mean_std.values()])
    std_array = np.array([value[1] for value in mean_std.values()])
        
    plt.hist(size_array, bins=bin_nums, weights=mean_array, density=True, histtype='bar', alpha=0.75)

    plt.xlabel('Size of complex')
    plt.ylabel('Frequency')
    if save_fig:
        plt.save_fig('histgram_size_of_complex.png', dpi=300)
    if show_fig:
        plt.show()
    return size_array, mean_array, std_array