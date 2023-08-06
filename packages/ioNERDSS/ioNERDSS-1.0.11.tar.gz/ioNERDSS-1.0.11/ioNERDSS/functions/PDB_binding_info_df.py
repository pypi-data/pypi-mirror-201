import pandas as pd


def PDB_binding_info_df(inp_name):
    status = False
    index = -1
    binding_info = pd.DataFrame(
        columns=['Protein_Name_1', 'Cite_Name_1', 'Protein_Name_2', 'Cite_Name_2', 'sigma'])
    with open(inp_name, 'r') as file:
        for line in file.readlines():
            if line == 'end reactions\n':
                status = False
                break
            if line == 'start reactions\n':
                status = True
            if status:
                if '<->' in line:
                    index += 1
                    line1 = line.split('+')
                    element1 = line1[0].strip(' ')
                    line2 = line1[1].split('<->')
                    element2 = line2[0].strip(' ')
                    element1_ = element1.strip(')').split('(')
                    element2_ = element2.strip(')').split('(')
                    binding_info.loc[index,
                                     'Protein_Name_1'] = element1_[0][0:3]
                    binding_info.loc[index, 'Cite_Name_1'] = element1_[1][0:3]
                    binding_info.loc[index,
                                     'Protein_Name_2'] = element2_[0][0:3]
                    binding_info.loc[index, 'Cite_Name_2'] = element2_[1][0:3]
                if 'sigma' in line:
                    binding_info.loc[index, 'sigma'] = float(
                        line.split(' = ')[-1].strip('\n'))
    return binding_info


