from base_regressor import baseRegressor
from text_to_list import list_correct
from excess_functions import return_single_column

df = list_correct()
# 268 & 267 are regression problems
# 266 is a classification problem

DAT = 268;

# Taking the first 20 variance problems
wt = [12, 21, 267, 25, 266, 20, 11, 28, 27, 16, 26, 32, 13, 29, 2, 33, 1, 17, 30, 14]

# Toy Data
#df = [ ["P1",1,2,10],["P2",3,5,26],["P3",1,1,6],["P4",6,2,20],["P5",5,3,22] ]
# [0,1,2,3]

model = baseRegressor(raw_data=df,feature_stop=265,target_column=DAT,
                      regressor=True,features_to_use=wt,stoppage=10000000);
model.fit(alpha=0.000000000001,target_error=1); # Best I could find for 268
"""
model = baseRegressor(raw_data=df,feature_stop=265,target_column=266,
                      regressor=False,features_to_use=wt);
model.fit(alpha=0.00000000001,target_error=0.1);   # For Classification
"""

print model.weights;     # Returns a list of random values.
l = map(abs, model.weights);
#print "Should return 2,4"

#print model.baseError_plot # this is a list

b = sorted(range(len(l)),key=lambda k: l[k]);
b.reverse()
print b;

ys = return_single_column(df,dex=DAT);
print ys[0:10];
print model.predict(df[0:10]);




