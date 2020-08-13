# TPOTClassifier(verbosity=2,generations=100,config_dict={'sklearn.linear_model.LogisticRegression': {}},max_time_mins=1,random_state=42,early_stop=3)# ifile data/TK.csv  model=LR Tpot_file=data/TK_100g_LR_Tpot.py, Tpot_score=0.2119700748129676, starttime2020-08-12 17:53:51.395874, endtime=2020-08-12 17:54:53.320106 duration=0:1:1
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: 0.4944583940428816
exported_pipeline = LogisticRegression()
# Fix random state in exported estimator
if hasattr(exported_pipeline, 'random_state'):
    setattr(exported_pipeline, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
