# TPOTClassifier(verbosity=2,generations=100,config_dict={'sklearn.naive_bayes.GaussianNB': {}, 'sklearn.naive_bayes.BernoulliNB': {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0], 'fit_prior': [True, False]}, 'sklearn.naive_bayes.MultinomialNB': {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0], 'fit_prior': [True, False]}},max_time_mins=1,random_state=42,early_stop=3)# ifile data/TK.csv  model=Tpot_Gauss Tpot_file=data/TK_100g_Tpot_Gauss_Tpot.py, Tpot_score=0.30798004987531175, starttime2020-08-05 17:54:28.756950, endtime=2020-08-05 17:55:30.390137 duration=0:1:1
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: 0.5845112425444835
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=BernoulliNB(alpha=100.0, fit_prior=True)),
    BernoulliNB(alpha=0.001, fit_prior=True)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
