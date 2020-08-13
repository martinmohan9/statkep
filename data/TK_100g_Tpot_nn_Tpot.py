# TPOTClassifier(verbosity=2,generations=100,config_dict=TPOT NN,max_time_mins=None,random_state=42,early_stop=3)# ifile data/TK.csv  model=Tpot_nn Tpot_file=data/TK_100g_Tpot_nn_Tpot.py, Tpot_score=0.32917705735660846, starttime2020-07-25 13:09:12.147402, endtime=2020-07-25 13:09:30.048043 duration=0:0:17
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: 0.3801595437329509
exported_pipeline = GaussianNB()
# Fix random state in exported estimator
if hasattr(exported_pipeline, 'random_state'):
    setattr(exported_pipeline, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
