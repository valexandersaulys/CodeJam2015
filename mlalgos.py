"""
Basic Linear Regressor object.

Pseudocode Below:
-----------------
set alpha (learning rate)
while error > some_target_error
loop over subject
extract features, put into [x]
initialize weights as [w]
make own function?
extract target value as y_true
call dot_product([w]*[x]), put value into y_pred
set [w] to [w] + alpha*y_pred*[x]
set some_target_error to y_true - dot_product([w]*[x]) 
"""

from random import uniform
import math

class baseRegressor():

    def __init__(self,
                 raw_data,
                 feature_stop,
                 target_column,
                 regressor=True,
                 existing_weights="nope",
                 features_to_use="all"):

        self.yf = target_column;   # Column that holds the target data
        self.fs = feature_stop;    # first column is patient_id, go until this column
        self.raw_data = raw_data;  # Holds training data
        self.patients = len(raw_data);

        self.regressor = regressor;  # True if regressor, False if classifier
        self.baseError_plot = [];

        if features_to_use == "all":
           test_subject = raw_data[0] # Should return first subject
           self.features_to_use = range(1, len(test_subject[0:feature_stop+1]));  # Excluding first, which is patient ID
        else:
            self.features_to_use = features_to_use;

        if existing_weights == "nope":
            self.weights = self.initialize_weights([-0.01,0.01]);
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
                # alpha * (true - predicted)
                # this might be predicted minus true, in case there's trouble
                update = self.mp(x_train,alpha*(y_true[i] - y_pred[i]));
                new_weights = self.ap(self.weights, update);
                self.weights = new_weights;

                i += 1 # Update counter variable
            
            #baseError = abs(sum(y_true)) - abs(sum(y_pred));
            baseError = sum(self.abs_sp(y_true,y_pred)); # Above might be the same
            print baseError;
            print j;
            print "-------"
            j += 1;

            if j > 100000:
                break;

    
    def predict(self,newdata):
        # Assume newdata is structured like the old data
        x_train = newdata[self.features_to_use]
        y_pred = self.dp(self.weights,x_train);
        return y_pred;


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



