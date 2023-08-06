def real_PDB_show_PDB(Result: bool):
    reaction_chain, int_site, int_site_distance, unique_chain, COM = Result
    f = open('show_structure.pdb', 'w')
    f.write('TITLE  PDB\n')
    f.write('REMARK   0 THE COORDINATES IN PDB FILE IS IN UNIT OF ANGSTROM, \n')
    f.write('REMARK   0 SO THE VALUE WILL BE 10 TIMES LARGER THAN NERDSS INPUTS.\n')
    tot_count = 0
    for i in range(len(unique_chain)):
        f.write('ATOM' + ' '*(7-len(str(tot_count))) + str(tot_count) + '  COM' +
                '   ' + unique_chain[i] + ' '*(5-len(str(i))) + str(i) +
                ' '*(13-len(str(round(COM[i][0]*10, 3)))) + str(round(COM[i][0]*10, 3)) +
                ' '*(8-len(str(round(COM[i][1]*10, 3)))) + str(round(COM[i][1]*10, 3)) +
                ' '*(8-len(str(round(COM[i][2]*10, 3)))) + str(round(COM[i][2]*10, 3)) +
                '     0     0CL\n')
        tot_count += 1
        for j in range(len(reaction_chain)):
            if unique_chain[i] in reaction_chain[j]:
                if unique_chain[i] == reaction_chain[j][0]:
                    # react_site = reaction_chain[j][1].lower()
                    react_coord = int_site[j][0]
                else:
                    # react_site = reaction_chain[j][0].lower()
                    react_coord = int_site[j][1]
                react_site = reaction_chain[j][0].lower(
                ) + reaction_chain[j][1].lower()
                f.write('ATOM' + ' '*(7-len(str(tot_count))) + str(tot_count) +
                        ' '*(5-len(str(react_site))) + str(react_site) +
                        '   ' + unique_chain[i] + ' '*(5-len(str(i))) + str(i) +
                        ' '*(13-len(str(round(react_coord[0]*10, 3)))) + str(round(react_coord[0]*10, 3)) +
                        ' '*(8-len(str(round(react_coord[1]*10, 3)))) + str(round(react_coord[1]*10, 3)) +
                        ' '*(8-len(str(round(react_coord[2]*10, 3)))) + str(round(react_coord[2]*10, 3)) +
                        '     0     0CL\n')
                tot_count += 1
    print('PDB writing complete! (named as show_structure.pdb)')
    return 0


