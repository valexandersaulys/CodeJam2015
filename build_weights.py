"""
This code will build the necesary weights desired

# 268 & 267 are regression problems
# 266 is a classification problem
"""

from base_regressor import baseRegressor
from text_to_list import list_correct, splitter, return_single_column
from excess_functions import return_single_column

def binary_cv(l1,l2):
    # Assuming both lists are the same length
    total_count = len(l1); yes_count = 0;
    for i in range(total_count):
        if l1[i] == l2[i]:  # I guess it doesn't matter which are the predictions?
            yes_count += 1;
    return float(yes_count / float(total_count));

df = list_correct()
training, validation = splitter(df)

# Taking the first 20 variance problems
#wt = [12, 21, 267, 25, 266, 20, 11, 28, 27, 16, 26, 32, 13, 29, 2, 33, 1, 17, 30, 14]
wt = [12, 21, 25, 20, 11, 28, 27, 16, 26, 32, 13, 29, 2, 33, 1, 17, 30, 14]
# categorical: [ 1, 4, 5, 6, 7, 8, 9, 10, 11 ] x
# 11 is treatments (1,2,3,4,5,6) categories

# I changed alpha by 1 decimal place
# Below will be the classification problem
model = baseRegressor(raw_data=training,feature_stop=265,target_column=266,
                      regressor=False,features_to_use=wt,stoppage=5000000);
model.fit(alpha=0.0000000001,target_error=0.1);   # For Classification

print model.weights;   # Need to test that I can insert weights correctly here

predictions = model.predict(validation);
answers = return_single_column(validation,dex=266);
print "Percentage Correct: " + str(binary_cv(predictions,answers));

"""
# This will train for the first regressive value
model = baseRegressor(raw_data=df,feature_stop=265,target_column=267,
                      regressor=True,features_to_use=wt,stoppage=10000000);
model.fit(alpha=0.000000000001,target_error=1); # Best I could find for 268
 
# This will train for the last regressive value
model = baseRegressor(raw_data=df,feature_stop=265,target_column=268,
                      regressor=True,features_to_use=wt,stoppage=10000000);
model.fit(alpha=0.000000000001,target_error=1); # Best I could find for 268
"""

print model.weights;     # Returns a list of random values.

l = map(abs, model.weights);
b = sorted(range(len(l)),key=lambda k: l[k]);
b.reverse()
print b;  # Print out the most important features by weight

ys = return_single_column(df,dex=DAT);
print ys[0:10];
print model.predict(df[0:10]);  
