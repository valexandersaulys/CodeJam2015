"""
This implements a Gradient Boosting Machine
"""

from base_regressor import baseRegressor

class GradientBoostingMachine():

    def __init__(self,raw_data,
                 feature_stop,
                 target_column,
                 M=10,   # Number of imtes to loop GBM portion
                 regressor=True,
                 existing_weights="nope",
                 features_to_use="all"):
        # Instantiate the regModel first
        self.regModel = baseRegressor(raw_data,feature_stop,target_column,regressor,
                                      existing_weights,features_to_use);
        self.raw_data = raw_data;
        self.fs = feature_stop;
        self.tc = target_column;
        self.regressor = regressor;

        self.M = M;

        self.gamma = gamma;
        self.residModel = 0;
        

    def fit(self,alpha=0.001,target_error=0.001):
        # First fit for old fitting of F_0
        self.regModel.fit(self.raw_data,alpha=0.001,target_error=0.001);

        # Initial gamma
        gamma = self.gamma;
        
        # build r list to be as long as x data list
        r = []*len(raw_data);

        # Loop below parts for 1 to M times, define M in instantiation. 
        for i in range(self.M):
            # Find residuals
            # For Fitting Residuals 
            # r_im = 1/2 * summation( 2*True_i - 2*theta*x_i ) from i=1 to number of subjects
            # m for above is the number of patients, x_i changes as does x_i, 2 cancels out
            For j in range(len(r)):
                # take out each patient to find its residuals
                x_data = raw_data[j][self.features_to_use];
                y_data = raw_data[j][self.tc];

                placeholder = self.dp(regModel.weights,x_data);
                r[j] = -1 * (y_data - placeholder)  # -1 or not?

                
            # r will be the residuals, numbered as many as there are patients
            # --> len(rawdata) = len(residuals)
            # Fit new model object onto residuals, call new model residModel
            resid_data = []
            for j in range(len(r)):
                resid_data.append(raw_data[j][self.features_to_use] + r[j])
            residModel = baseRegressor(raw_data=resid_data,
                                       feature_stop=len(features_to_use),
                                       target_column=features_to_use + 1, 
                                       regressor=self.regressor);
        
            # Convert raw data just to the points we care about
            prim_data = [];
            for j in range(len(raw_data)):
                prim_data.append(raw_data[j][self.features_to_use];
                target_values = raw_data[j][self.tc];

            # find multiplier as the argmin( summation( L(true,F_m-1 + gamma*residModel) ) )
            gamma = self.minLoss(priModel,residModel,prim_data,resid_data,
                                 target_values,number_of_values,gamma);

            # Update F_m = F_m-1(x) + gamma*residModel(x)
            # regModel = F_m-1(x) & save residModel(x) and gamma as self
            self.residModel = residModel;
            self.regModel = regModel;
            self.gamma = gamma;
            


    def predict(self,newdata):
                                 
        preds = []

        for entry in newdata:
            
            pri = self.regModel.predict(entry);
            res = self.residModel.predict(entry);
            preds.append(pri + self.gamma*res);

        return preds;
        

    def minLoss(self,priModel,residModel,prim_data,resid_data,target_values,
                number_of_values,gamma,alpha=0.0001,max_iter=1000):
        """
        Minimizes the loses here
        """

        baseError = 10000000;
        i = 0;
        
        while i < max_iter;

            y_preds = []; y_trues = [];

            for i in range(number_of_values):
                x_pri = prim_data[0]; x_res = resid_data[0];
                
                precusor = self.mp(residModel.predict(resid_data),gamma);
                y_val = self.dp(priModel.predict(prim_data),precusor);
                
                y_preds.append(y_val);
                y_trues.append(target_values[i]);

                # Update gamma
                change = alpha*(target_values[i] - y_val);
                gamma = gamma + change;

                # Error Check for gamma
                print gamma;
                
                
            # Computer a base Error
            baseError = XXX;
            i += 1;

        print baseError;
        return gamma;


    def dp(self,a,b):    # Dot Product
        ab = [a[i]*b[i] for i in range(len(a))];
        return sum(ab);

    def mdp(self,a,b):    # Multiplied Lists
        ab = [a[i]*b[i] for i in range(len(a))];
        return ab;

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
    

    def sigmoid(self,x):   # Decision function for classifier
        return 1 / (1 + math.exp(-x))
