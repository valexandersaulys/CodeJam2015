"""
This code will build the necesary weights desired

# 268 & 267 are regression problems
# 266 is a classification problem
"""

from base_regressor import baseRegressor
from text_to_list import list_correct, splitter, return_single_column
from excess_functions import return_single_column

def mse(l1,l2):
    # Assuming both lists are the same length
    # l1 is the true values, l2 is the predicted values
    running_summation = 0;
    for i in range(len(l1)):
        running_summation += (l1[i] - l2[i])**2
    return float( (1/float(len(l1))) * running_summation );

df = list_correct()
training, validation = splitter(df)

# Taking the first 20 variance problems
#wt = [12, 21, 267, 25, 266, 20, 11, 28, 27, 16, 26, 32, 13, 29, 2, 33, 1, 17, 30, 14]
wt = [12, 21, 25, 20, 11, 28, 27, 16, 26, 32, 13, 29, 2, 33, 1, 17, 30, 14]
# categorical: [ 1, 4, 5, 6, 7, 8, 9, 10, 11 ] x
# 11 is treatments (1,2,3,4,5,6) categories

# This will train for the first regressive value
model = baseRegressor(raw_data=df,feature_stop=265,target_column=267,
                      regressor=True, existing_weights=[-0.10,0.10],
                      features_to_use=wt,stoppage=80000);
model.fit(alpha=0.0000000000001,target_error=0.00001); # Best I could find for 268
"""
# This will train for the last regressive value
model = baseRegressor(raw_data=df,feature_stop=265,target_column=268,
                      regressor=True,features_to_use=wt,stoppage=10000000);
model.fit(alpha=0.000000000001,target_error=1); # Best I could find for 268
"""

print model.weights;     # Returns a list of random values.
predictions = model.predict(validation);
answers = return_single_column(validation,dex=267);
print "Mean-Squared Error: " + str(mse(answers,predictions));


"""
l = map(abs, model.weights);
b = sorted(range(len(l)),key=lambda k: l[k]);
b.reverse()
print b;  # Print out the most important features by weight

ys = return_single_column(df,dex=DAT);
print ys[0:10];
print model.predict(df[0:10]);  
"""
