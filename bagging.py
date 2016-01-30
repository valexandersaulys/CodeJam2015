"""
Test the base_regressor first!

Pseudocode:

Select m points from dataset S
fit model h to those points
Output combined classifier
"""
from random import randint
import random;

class baggingEstimator():

    def __init__(baseModel,
                 number_of_models,
                 subjects_per,
                 raw_data,
                 feature_stop,
                 target_column,
                 with_replacement=True,
                 regressor=True,
                 existing_weights="nope",
                 features_to_use="all"):

        self.baseModel = baseModel;  # Save the basic model being used, should be calleable
                                     # with .fit() function
        self.number_of_models = number_of_models; # Number of learners to train with bagging
        self.subjects_per = subjects_per  # number of subjects/entries per subset of data

        self.regressor = regressor;  # True if regressor, False if classifier
        self.target_values = raw_data[target_columns]  # Necesary for subsetting

        self.yf = target_column;   # Mark the column that contains the target values
        self.fs = feature_stop;    # First column is patient_id, go until stopped column
        self.raw_data = raw_data;  # Save raw_data, assumed to be list of lists
        self.max_subjects = len(raw_data); # Find the number of subjects to save

        if features_to_use == "all":
           test_subject = raw_data[0]; # Should return first subject
           
           # Excluding first, which is patient ID
           self.features_to_use = range(1, len(test_subject[1:feature_stop]));
        
       else:
            self.features_to_use = features_to_use;  # otherwise a list of the features to be used


    def fit(alpha=0.01,target_error=0.001):
        # Build subset S from rawdata
        # predict m models each on its own subset
        # save each model, return some aggregate (average for now);
        m = [0] * len(self.number_of_models);

        for i in range(self.number_of_models);
            # Build subset of data
            """
            w/o replacement --> random.sample(xrange(max_int),num_in_list);
            with replacement --> my_randoms = [random.randrange(1,101,1) for _ in range(10)]
            """
            if with_replacement == False:
                vals = random.sample(xrange(self.max_subjects),subjects_per);
            else:
                vals = [random.randrange(0,self.max_subjects,1) for _ in range(subjects_per)]
            t_vals = self.target_values[vals]
            subset_data = raw_data[vals] + t_vals # should take just the listed values here

            m[i] = baseModel(subset_data,
                             feature_stop=subjects_per+1,   # Just have one user extra?
                             target_column=subjects_per+2,  # Target column to use?
                             existing_weights="nope",
                             features_to_use="all");
                             
            m[i].fit(alpha,target_error);


    def predict(newdata):
        # Assume newdata is structured like the old data
        x_train = newdata[features_to_use]
        y_preds = [0] * len(x_train)  # return list of predictions

        for i in range(len(y_preds)):
            y_preds[i] = self.dp(self.weights,x_train[i]);

        # Now return the values
        if self.regressor == True:
            return y_preds;

        else: # classification
            # This will return 1 or 0, not 1 or -1 like we're encoding (may be confusing)
            for i in range(len(y_preds)):
                y_preds[i] = round(sigmoid(y_preds));
            
            return y_preds; 
                

    def initialize_weights(stuff):
        weights = [0] * self.number_features
        
        for i in self.number_features:
            weights[i] = uniform(stuff[0],stuff[1]);

        return weights;
    

    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    # = = = = = = = = = = = LINEAR ALGEBRA FUNCTIONS = = = = = = = = = = = = #
    def dp(a,b):    # Dot Product
        ab = [a[i]*b[i] for i in range(len(a))];
        return sum(ab);

    def ap(a,b):   # addition of two arrays
        ab = [a[i]+b[i] for i in range(len(a))];
        return ab;

    def mp(a,b):   # assuming b is a value and a is a list of values
        ab = [a[i]*b for i in range(len(a))];
        return ab;
