# TPOTClassifier(verbosity=2,generations=100,config_dict=TPOT light,max_time_mins=None,random_state=42,early_stop=3)# ifile data/TK_vif.csv  model=Tpot_light Tpot_file=data/TK_vif_100g_Tpot_light_Tpot.py, Tpot_score=0.27680798004987534, starttime2020-07-25 12:54:56.465902, endtime=2020-07-25 12:55:01.043311 duration=0:0:4
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: 0.5020763145416884
exported_pipeline = KNeighborsClassifier(n_neighbors=21, p=1, weights="distance")
# Fix random state in exported estimator
if hasattr(exported_pipeline, 'random_state'):
    setattr(exported_pipeline, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
