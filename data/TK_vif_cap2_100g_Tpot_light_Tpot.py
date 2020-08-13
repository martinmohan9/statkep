# TPOTClassifier(verbosity=2,generations=100,config_dict=TPOT light,max_time_mins=1,random_state=42,early_stop=3)# ifile data/TK_vif_cap2.csv  model=Tpot_light Tpot_file=data/TK_vif_cap2_100g_Tpot_light_Tpot.py, Tpot_score=0.33541147132169574, starttime2020-07-21 11:03:12.677324, endtime=2020-07-21 11:03:30.545981 duration=0:0:17
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: 0.8025794599201802
exported_pipeline = DecisionTreeClassifier(criterion="gini", max_depth=7, min_samples_leaf=20, min_samples_split=4)
# Fix random state in exported estimator
if hasattr(exported_pipeline, 'random_state'):
    setattr(exported_pipeline, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
