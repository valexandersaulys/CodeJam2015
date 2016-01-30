#!/usr/bin/env python

from random import uniform
import math

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
    """
    if textfile == input:
        #f = sys.stdin
        #f = open('trainingData.txt', 'rU')
    else: f = open('trainingData.txt', 'rU')
    """
    f = sys.stdin
    
    rawdata_table = []
    
    # Skip first two rows from table
    # Save row with all parameter IDs to title_row in case we need it later
    # Also prevents fuck ups when replacing 'ND' in list_corect function
    """
    line = f.readline()
    title_row = f.readline().split()
    """
    line = f.readline()                 
    #Remainder of rows (actual data) are put into a list       
    while line:
        rawdata_table.append(line.split())
        line = f.readline()  

    return rawdata_table

###############################################################################
	
def list_correct(textfile="gurrr"):
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

def translate_to_words(l):
    for i in range(len(l)):
        if l[i] == float(1):
            l[i] = "COMPLETE_REMISSION"
        elif l[i] == float(-1):
            l[i] = "RESISTANT";
    return l;


# Add in objects
class baseRegressor():

    def __init__(self,
                 raw_data,
                 feature_stop,
                 target_column,
                 regressor=True,
                 existing_weights="nope",
                 features_to_use="all",
                 stoppage=100000):

        self.yf = target_column;   # Column that holds the target data
        self.fs = feature_stop;    # first column is patient_id, go until this column
        self.raw_data = raw_data;  # Holds training data
        self.patients = len(raw_data);

        self.regressor = regressor;  # True if regressor, False if classifier
        self.baseError_plot = [];
        self.stoppage = stoppage;

        if features_to_use == "all":
           test_subject = raw_data[0] # Should return first subject
           self.features_to_use = range(1, len(test_subject[0:feature_stop+1]));  # Excluding first, which is patient ID
        else:
            self.features_to_use = features_to_use;

        if existing_weights == "nope":
            self.weights = self.initialize_weights([-1.0,1.0]);
        elif len(existing_weights) == 2:
            self.weights = self.initialize_weights(existing_weights);
        else:
            self.weights = existing_weights;


    def fit(self,alpha=0.0001,target_error=0.001):
        baseError = 1000000;
        change = 0; N = float(self.patients); j = 1;
        
        while abs(baseError) > abs(target_error): 

            y_pred = []; y_true = []; i = 0;

            for subject in self.raw_data:
                # Take out features we wish to use 
                x_train = [subject[x] for x in self.features_to_use]

                # First find the predicted value, add it to the list
                y_pred.append(self.dp(self.weights, x_train));
                y_true.append(subject[self.yf]);

                # Find rate of error
                baseError = abs(y_true[i] - y_pred[i]);
                
                # Calculate the update rule
                # alpha * (true - predicted) * x_train
                # this might be predicted minus true, in case there's trouble
                update = self.mp(x_train,alpha*(y_true[i] - y_pred[i]));
                new_weights = self.ap(self.weights, update);
                self.weights = new_weights;

                i += 1 # Update counter variable
            
            #baseError = abs(sum(y_true)) - abs(sum(y_pred);)
            baseError = sum(self.abs_sp(y_true,y_pred)); # Above might be the same
            print baseError;
            print j;
            print "-------"
            j += 1;

            if j > self.stoppage:
                break;

    
    def predict(self,newdata):
        y_preds = []; 

        # Assume newdata is structured like the old data
        for i in range(len(newdata)):
            x_train = [newdata[i][x] for x in self.features_to_use]
            val = self.dp(self.weights,x_train)

            if self.regressor ==True:
                y_preds.append(val);
            else:
                if val < 0:
                    y_preds.append(float(-1.0));
                if val > 0:
                    y_preds.append(float(1.0));
        
        return y_preds;


    def dp(self,a,b):    # Dot Product
        ab = [a[i]*b[i] for i in range(len(a))];
        return sum(ab);

    def ap(self,a,b):   # addition of two arrays
        ab = [a[i]+b[i] for i in range(len(a))];
        return ab;

    def mp(self,a,b):   # assuming b is a value and a is a list of values
        ab = [a[i]*b for i in range(len(a))];
        return ab;

    def sp(self,a,b):   # subtraction of two arrays
        ab = [a[i]-b[i] for i in range(len(a))];
        return ab

    def abs_sp(self,a,b):
        ab = [abs(a[i])-abs(b[i]) for i in range(len(a))];
        return ab                

    def initialize_weights(self,stuff=[]):
        weights = [0] * len(self.features_to_use);
        
        for i in range(len(weights)):
            weights[i] = uniform(stuff[0],stuff[1]);

        return weights;
    
    def sigmoid(self,x):   # Decision function for classifier
        return 1 / (1 + math.exp(-x))


def main():

    import sys;

    testData = list_correct()

    # Features to use
    features = [12, 21, 25, 20, 11, 28, 27, 16, 26, 32, 13, 29, 2, 33, 1, 17, 30, 14]

    # Paste in weights
    wt_class = [0.005282546933085302, 
    0.00019005094290200331, 
    -0.3208438520005847, 
    0.060298374167868034, 
    0.47575278102153445, 
    -0.007341090879961012, 
    -0.0003345576888578404, 
    -0.34825960673644474, 
    0.0003877180341366817, 
    -0.28494755094203117, 
    2.964726478234287e-06, 
    -0.01292471641406875, 
    0.0005911449483264154, 
    0.008637346773164302, 
    0.1367495624114614, 
    0.004521909748139259, 
    -0.009062774664435601, 
    -0.01652866109254906]
    
    wt_reg2 = [-1.4782528679688447, 
    0.45690984327639694, 
    0.08869480773275684, 
    2.1565270328816384, 
    1.2915888943947875, 
    -0.06372457343712974, 
    0.3499929711891729, 
    0.8237023625971672, 
    0.05162940011374745, 
    0.1688508314397867, 
    0.00012726053658120771, 
    -0.35924914261045215, 
    -1.0769690349274155, 
    1.047386146930229, 
    -0.19964400719516762, 
    0.9795098488465421, 
    0.2014420625498814, 
    -0.27627124946984455]
    
    wt_reg1 = [-0.18680892594219245, 
    0.4548718121549312, 
    0.010645396682980634, 
    0.24184823925811158, 
    0.0017808211592471928, 
    0.6059705789542096, 
    0.21079453371259096, 
    0.139815606380712, 
    0.05781631793747934, 
    -0.012928360566733191, 
    -0.000369868737672888, 
    -0.01610784274975732, 
    -0.467868433330037, 
    0.6990894422659071, 
    0.06469358505487681, 
    0.6096663873337065, 
    -0.11545799126589541, 
    0.11441317491154322] 

    # Build Models, paste in weights to initialize
    cl_model = baseRegressor(raw_data=testData,
                        feature_stop=265,
                        target_column=266,
                        regressor=False,
                        existing_weights=wt_class,
                        features_to_use=features);
    
    reg2_model = baseRegressor(raw_data=testData,
                        feature_stop=265,
                        target_column=267,
                        regressor=True, 
                        existing_weights=wt_reg2,
                        features_to_use=features);
    
    reg1_model = baseRegressor(raw_data=testData,
                        feature_stop=265,    # This are meaningless
                        target_column=268,   # This too
                        regressor=True,    # It is a regressor 
                        existing_weights=wt_reg1,
                        features_to_use=features);

    # Predict one by one & gather results


    # Results should be three lists for each predicted value
    preds_class = cl_model.predict(testData)
    preds_reg2 = reg2_model.predict(testData)
    preds_reg1 = reg1_model.predict(testData)

    # convert classification to list of "COMPLETE_REMISSION" or "RESISTANT"
    preds_class = translate_to_words(preds_class)

    # Write out line by line using loop
    for i in range(len(testData)):
        patient_name = testData[i][0]

        # Keep in mind that reg2 will be zero if RESISTANT
        if preds_class[i] == "RESISTANT":
            reg2 = 0.0;
        else:
            reg2 = preds_reg2[i] / 100.0;

        reg1 = preds_reg1[i] / 8.5;
        clasp = preds_class[i]

        # Write out final results
        sys.stdout.write("%s\t%s\t%2.2f\t%2.2f\n" % (patient_name,clasp,reg2,reg1) )


if __name__ == "__main__":
    main();