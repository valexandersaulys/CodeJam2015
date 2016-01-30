def return_single_column(lol,dex=1):
    # Assuming lol is a list of lists
    # returns a single column indexed as dex
    single_col = [0] * len(lol);
    for i in range(len(single_col)):
      single_col[i] = lol[i][dex]
    return single_col;
 
def unique_value_dict (clist): 
# Given the data table, go to 11th column, get rid of duplicates and sort in dictionary
    trtmnt = return_single_column(clist,dex=11)
    set_trtmnt = list(set(trtmnt))
    d = {} ; x = 1    
    for y in set_trtmnt:
        d[y] = x
        x += 1    
    return d
    
def text_to_list():
# text_to_list function:
## Converts trainingData.txt input file to 2D list
## Primary categorization by row (i.e. by patient)
## Secondary categorization by column (i.e. by parameter)
## List output: [[Patient01, p1, p2, ...], [Patient02, p1, p2, ...], ...]
## Where p1, p2, etc are the parameters

    rawdata_table = []
    with open('trainingData.txt', 'rU') as f:
        # Skip first two rows from table
        # Save row with all parameter IDs to title_row in case we need it later
        # Also prevents fuck ups when replacing 'ND' in list_corect function
        line = f.readline()
        title_row = f.readline().split()
        line = f.readline()                
        #Remainder of rows (actual data) are put into a list       
        while line:
            rawdata_table.append(line.split())
            line = f.readline()  

    return rawdata_table

def list_correct():
# .replace function doesn't work to convert string to number
    import copy 
    rlist = text_to_list()          #convert txt file to list (strings)
    clist = copy.deepcopy(rlist)    #copy list to new list

    d = unique_value_dict(clist)    # classifies treatments in dictionary for easy sorting
    
    # Convert non-numerical values to assigned values (1, 0 -1)
    # Convert treatment to values 1 through 5 using dictionary
    # Convert remaining numerical strings to floats    
    for patient in clist:
        for i in range(len(patient)):
            j = patient[i]            
            if i == 0: 
                continue
            if j =='YES' or j =='Yes' or j == 'POS' or j == 'COMPLETE_REMISSION' or j == 'F':
                patient [i] = 1.0
            if j =='NO' or j =='No' or j == 'NEG' or j == 'RESISTANT' or j == 'M':
                patient [i] = -1.0
            if j == 'NA' or j == 'ND' or j == 'NotDone':
                patient [i] = 0.0           
            if i == 11:
                patient [i] = d[patient[i]]
            
            else: patient[i] = float(patient[i])

    return clist
       
         
#    t = open('datalist.txt', 'w')    
#    for row in rawdata_table:
#        t.write('%s\n' % row)
#    t.close()
#    print len(rawdata_table)


