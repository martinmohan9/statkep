# TPOTClassifier(verbosity=2,generations=100,config_dict=None,max_time_mins=None,random_state=42,early_stop=3)# ifile data/TK_vif.csv  model=None Tpot_file=data/TK_vif_100g_None_Tpot.py, Tpot_score=0.327930174563591, starttime2020-07-17 19:04:26.030415, endtime=2020-07-18 13:15:32.443692 duration=18:11:6
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from xgboost import XGBClassifier
from tpot.export_utils import set_param_recursive

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: 0.8585496320953384
exported_pipeline = make_pipeline(
    SelectPercentile(score_func=f_classif, percentile=82),
    XGBClassifier(learning_rate=0.1, max_depth=6, min_child_weight=20, n_estimators=100, nthread=1, subsample=0.9000000000000001)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
