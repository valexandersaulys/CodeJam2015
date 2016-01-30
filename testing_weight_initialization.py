from base_regressor import baseRegressor
from text_to_list import list_correct
df = list_correct()

model = baseRegressor(raw_data=df,feature_stop=265,target_column=266,
                      regressor=False,features_to_use=[3,4,5,6],
                      existing_weights = [6.0,3.0,4.0,5.0],
                      stoppage=10000000);

print model.weights;
