## LEFT TO DO: FIGURE OUT HOW TO INTEGRATE SYSSTDIN WITH text_to_list function
###############################################################################
#TEST CODE FOR LISTS - Open file in excel to quickly make sure matches w/ original
#    t = open('datalist.txt', 'w')    
#    for row in rawdata_table:
#        t.write('%s\n' % row)
#    t.close()
#    print len(rawdata_table)

###############################################################################

def return_single_column(lol,dex=1):
    # Assuming lol is a list of lists
    # returns a single column indexed as dex
    single_col = [0] * len(lol);
    for i in range(len(single_col)):
      single_col[i] = lol[i][dex]
    return single_col;

###############################################################################
 
def unique_value_dict (clist): 
# Given the data table, go to 11th column, get rid of duplicates and sort in dictionary
    trtmnt = return_single_column(clist,dex=11)
    set_trtmnt = list(set(trtmnt))
    d = {} ; x = 1    
    for y in set_trtmnt:
        d[y] = x
        x += 1    
    return d
    
###############################################################################
    
def text_to_list(textfile):
# text_to_list function:
## If argument is 'input': should open file as sys.stdin
## Else, it should just open the trainingData.txt
##Converts trainingData.txt input file to 2D list
## Primary categorization by row (i.e. by patient)
## Secondary categorization by column (i.e. by parameter)
## List output: [[Patient01, p1, p2, ...], [Patient02, p1, p2, ...], ...]
## Where p1, p2, etc are the parameters
    import sys
    
    if textfile == input:
       #f = sys.stdin
        f = open('trainingData.txt', 'rU')
    else: f = open('trainingData.txt', 'rU')
	
    rawdata_table = []
    
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

###############################################################################
	
def list_correct(textfile=input):
#Takes list from text_to_list() and transforms it so it can be used and read

    import copy 
    rlist = text_to_list(textfile)  #convert txt file to list (strings)
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

###############################################################################
 
def Branch (table, col, f=-3, t=1):
        
    import copy    
    ctable = copy.deepcopy(table)
    # make sorted list of all parameter values w/o duplicates
    set_values = sorted(list(set(return_single_column(table,dex=col))))
    # extreme values from sorted list determine if range is +/-     
    minm = set_values[0] ; maxm = set_values[-1]
    p_n = minm*maxm
    values = []    

    for row in ctable:
        values.append([row[col], row[f]])
    
    #split_pt = split_pt_finder(table, col, f, t)    
    split1 = split2 = split0 = []
    
    
    #print set_values
    if len(set_values) <= 3 or p_n < 0:
        split1 = [x for x in values if x[0] > 0]
        split2 = [x for x in values if x[0] < 0]
        split0 = [x for x in values if x[0] == 0]
    else:
        split1, split2, split0, acc, split_pt, one_or_two = pos_split_pt_finder(table, col)
        

    print len(split1) #+ 'points are bigger than 0'
    print len(split2) #+ 'points are smaller than 0'
    print len(split0) #+ 'points are equal to 0'
    print acc
    print split_pt
    print one_or_two
    
###############################################################################
   
def pos_split_pt_finder(table, col, f=-3, t=1):
    
    
    import copy    
    ctable = copy.deepcopy(table)
    # make sorted list of all parameter values w/o duplicates
    set_values = sorted(list(set(return_single_column(table,dex=col))))
    
    #create list with parameter of interest and criteria of interest (remission)
    values = []     
    for row in ctable:
        values.append([row[col], row[f]])
    
    #split_pt as point where list will be split, will be value from list
    #one_or_two indicates whethere the first or second split is more accurate
    #acc is a measure of accuracy (in this case, we maximize the # of resistants, s)  
    split_pt = 0    
    one_or_two = 1    
    a = b = s = avg_remission = sum(values[1])
    acc = 0
    print set_values
    #Try each unique parameter value as split_pt
    for index in set_values:
        split1 = [x for x in values if x[0] >= index and x[0] !=0]
        split2 = [x for x in values if x[0] < index and x[0]!=0]
        split0 = [x for x in values if x[0] == 0]
        
        a = sum( i[-1] for i in split1)
        #print split1
        #print a
        continue;
        
        b = sum( j[-1] for j in split2)
        if a > s or b > s:
            split_pt = index
            if a > s:
                one_or_two = 1
                s = a                
                acc = 0.5*(1+(s/len(values)))
            else:
                one_or_two = 2
                s = b                
                acc = 0.5*(1+(s/len(values)))
    
    split1 = [x for x in values if x[0] >= split_pt and x[0] !=0]
    split2 = [x for x in values if x[0] < split_pt and x[0]!=0]
    split0 = [x for x in values if x[0] == 0]    
    
    return split1, split2, split0, acc, split_pt, one_or_two
###############################################################################
   
def neg_split_pt_finder(table, col, f=-3, t=1):
    
    
    import copy    
    ctable = copy.deepcopy(table)
    # make sorted list of all parameter values w/o duplicates
    set_values = sorted(list(set(return_single_column(table,dex=col))))
    
    #create list with parameter of interest and criteria of interest (remission)
    values = []     
    for row in ctable:
        values.append([row[col], row[f]])
    
    #split_pt as point where list will be split, will be value from list
    #one_or_two indicates whethere the first or second split is more accurate
    #acc is a measure of accuracy (in this case, we maximize the # of remissions, s)
    split_pt = 0    
    one_or_two = 1    
    a = b = s = avg_remission = sum(values[1])
    acc = 0
   
    #Try each unique parameter value as split_pt
    for index in set_values:
        split1 = [x for x in values if x[0] >= index and x[0] !=0]
        split2 = [x for x in values if x[0] < index and x[0]!=0]
        split0 = [x for x in values if x[0] == 0]
        
        a = sum( i[-1] for i in split1)
        b = sum( j[-1] for j in split2)
        if a < s or b < s:
            split_pt = x
            if a < acc:
                one_or_two = 1
                s = a
                acc = 0.5*(1+(s/len(values)))
            else:
                one_or_two = 2
                s = b
                acc = 0.5*(1+(s/len(values)))
            
    split1 = [x for x in values if x[0] >= split_pt and x[0] !=0]
    split2 = [x for x in values if x[0] < split_pt and x[0]!=0]
    split0 = [x for x in values if x[0] == 0]
    
    return split1, split2, split0, acc, split_pt, one_or_two        

###############################################################################

def splitter(table, f=0.7, p=0):
    
    import random
    
    indic = range(0,len(table))
    cutoff = int(0.7*len(table))    
    
    random.shuffle(indic)
    
    tData = []
    vData = []   
   
    j = 0
    k = 0 
    #print table
    
    while k < len(table):
        row = indic[k]     
        if j <= cutoff:
            tData.append(table[row])
            j +=1
        else:
            vData.append(table[row])
        k += 1
    """
    print len(tData)
    print len(vData)
    print cutoff
    print indic
    print vData
    """
    return tData, vData;
    









      
