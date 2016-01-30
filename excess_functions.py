# = = = = = = = = = = = Sigmoid Function = = = = = = = = = = #
import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))



# = = = = = = = = = = = Linear Algebra Bits = = = = = = = = = = = = #
def dp(a,b):    # Dot Product
    ab = [a[i]*b[i] for i in range(len(a))];
    return sum(ab);

def ap(a,b):   # addition of two arrays
    ab = [a[i]+b[i] for i in range(len(a))];
    return ab;

def mp(a,b):   # assuming b is a value and a is a list of values
    ab = [a[i]*b for i in range(len(a))];
    return ab;


# = = = = = = = = = = = Data Manipulation = = = = = = = = = = = = #
def return_single_column(lol,dex=1):
    # Assuming lol is a list of lists
    # returns a single column indexed as dex
    single_col = [0] * len(lol);
    for i in range(len(single_col)):
      single_col[i] = lol[i][dex]
    return single_col;

def return_variance(col):
    # Returns variance of single list col
    avg = sum(col)/len(col);
    numerator = 0; denominator = len(col);
    for entry in col:
        numerator = numerator + (entry - avg)**2
    return numerator/float(denominator);

def noVariance(lol,min_variance,print_vars=True):
    # Returns columns that meet a threshold variance, drops ones that do not, return new lol

    # Loop through every patient, only take the values that are on the list
    
    new_lol = [];  # This will eventually be returned
    var_list = []; # Find list of variances for each column


    for col in lol:
        # Find the variance of each column
        var_list.append(return_variance(col));

    # Make a list of columns that make the minimum variance list(set(list1) - set(list2))
    min_var_cols = [var_list[i]>min_variance for i in j] # will return list of trues, falses
    cols_to_take = [];  # Will hold the columns to take (integers);

    # Loop through all the variance trues or falses, if true, add its index location to list
    # of values to take from. This loop returns a list of the indexes of values we want.
    for i in range(len(min_var_cols)):
        if min_var_cols[i]==True:
            cols_to_take.append(i);
    
    # Loop through every patient and only take the columns we want
    for col in lol:
        new_lol.append(col[cols_to_take])

    if print_vars==True:
        print var_list;

    return new_lol;


def list_variances(lol):
    # adjust weights based on positive/negative sweep?
    var_list = []; # Find list of variances for each column

    for i in range(len(lol[0])):
        col = return_single_column(lol,dex=i);
        if i != 0:
            # Find the variance of each column
            var_list.append(return_variance(col));

    return var_list;


# = = = = = = = = = = FINAL DECISION MAKER = = = = = = = = #
def final_decision_maker(target_values):
    # COMPLETE_REMISSION if 1
    # RESISTANT if 0
    return_vals = [];
    
    for val in target_values:
        if val == 1:
            return_vals.append("COMPLETE_REMISSION");
        elif val == 0:
            return_vals.append("RESISTANT");
        else:
            raise ValueError("Value %f passed" % val);

    return return_vals;

