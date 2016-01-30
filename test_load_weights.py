from base_regressor import baseRegressor
from text_to_list import list_correct, splitter
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

wt = [12, 21, 25, 20, 11, 28, 27, 16, 26, 32, 13, 29, 2, 33, 1, 17, 30, 14]
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

model = baseRegressor(raw_data=training,
                      feature_stop=3,
                      target_column=4,
                      regressor=False,
                      existing_weights=wt_class,
                      features_to_use=wt);

predictions = model.predict(validation);
answers = return_single_column(validation,dex=266);
print "Percentage Correct: " + str(binary_cv(predictions,answers));
