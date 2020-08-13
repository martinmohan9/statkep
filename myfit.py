#!/home/admin/anaconda3/bin/python3
#   author:martinmhan@yahoo.com date:  05/07/2020
#   Copyright (C) <2020>  <Martin Mohan>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#print(__doc__)
import joblib,argparse,re,sys,glob,os,time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from itertools import cycle
import json
import pickle
import mmodels

class myfit():
    """ Given a csv and model this will select the correct classifier.
    The user can train data and predict results on the model
    This uses the class mmodels

    """
    def __init__(self,fit,model="RF"):
        """
        At initialization the user select the input file and the model.
        If the input file begins with 'data/bT' so must the model name
        A name for the output files is generated based on these names.

        """

        self.bTK=False
        ifile=".csv"
        if("_cap2" in model):
            ifile="_cap2"+ifile
        else:
            pass

        if("_vif" in model):
            ifile="_vif"+ifile
        else:
            pass

        if(model.startswith("b")):
            self.bTK=True
            ifile="data/bTK"+ifile
        else:
            ifile="data/TK"+ifile
        self.ifile=ifile

#        self.ofile=ifile.replace(".csv", "_"+model) # basename 
        self.ofile="data/"+model # basename 
        self.model=mmodels.mmodels(model)

        ########################
#        self.df=pd.read_csv(self.ifile,comment='#')
#        self.y=self.df['koi_disposition'].reset_index(drop=True)
#        self.X=self.df.drop(['kepid','koi_disposition','kepoi_name'], axis=1).reset_index(drop=True)
#        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.1, random_state=42)

        self.df=pd.read_csv(self.ifile,comment='#')
        self.y=self.df['koi_disposition'].reset_index(drop=True)
        self.X=self.df.drop(['kepid','koi_disposition','kepoi_name'], axis=1).reset_index(drop=True)

        self.df_train, self.df_test = train_test_split(self.df, test_size=0.1,random_state=42)
        self.df_train=self.df_train.reset_index(drop=True)
        self.df_test=self.df_test.reset_index(drop=True)
        self.X_train=self.df_train.drop(['kepid','koi_disposition','kepoi_name'], axis=1).to_numpy()
        self.y_train=self.df_train['koi_disposition']
        self.X_test=self.df_test.drop(['kepid','koi_disposition','kepoi_name'], axis=1).to_numpy()
        self.y_test=self.df_test['koi_disposition']

        self.clf=self.fit_model(fit) # Train or load from pickle

    def train_split(self):
        return self.X_train,self.y_train,self.X_test,self.y_test

    def fit_model(self,fit):
        """ Train the model and pickle results.  """
        jobF=self.ofile+".pickle"
        classif=self.model.clf
    
        if fit:
            print(f"Fitting {self.model.name} to {jobF} using X_train and y_train")
            clf=classif.fit(self.X_train, self.y_train)
            pickle.dump( clf, open( jobF, "wb" ) )
        clf=pickle.load( open( jobF, "rb" ) )
        print(f"myfit.py: Loaded {self.model.name} from {jobF}")
        return clf

    def predict_results(self): # Use test data
        """ Run the model against 10% X_test,y_test data  """
        df=pd.DataFrame(self.clf.predict_proba(self.X_test), columns=self.clf.classes_)
        df['y_test']=pd.DataFrame(self.y_test)
        #df['y_test']=pd.DataFrame(self.y_test).reset_index(drop=True)
        df['y_pred']=pd.DataFrame(self.clf.predict(self.X_test))
        return df

    def overfit_results(self): # Use train data
        """ Run the model against 90% X_train,y_train data  
            The resulting dataframe should be similar to predict_results
            If it is not (too good) this indicates overfitting

        """
        df=pd.DataFrame(self.clf.predict_proba(self.X_train), columns=self.clf.classes_)
        df['y_test']=pd.DataFrame(self.y_train)
        #df['y_test']=pd.DataFrame(self.y_train).reset_index(drop=True)
        df['y_pred']=pd.DataFrame(self.clf.predict(self.X_train))
        return df

    def fit_all(self): # Use all data
        """ Run the model against all data / do split in train/test

        """
        df=pd.DataFrame(self.clf.predict_proba(self.X), columns=self.clf.classes_)
        df['y_test']=pd.DataFrame(self.y)
        #df['y_test']=pd.DataFrame(self.y).reset_index(drop=True)
        df['y_pred']=pd.DataFrame(self.clf.predict(self.X))
        return df

if __name__ == '__main__':
    """ The _main__ models is used for testing"""
#    mymodel=mmodels.mmodels("GB").desc
#    epilog=json.dumps(mymodel, indent=4, ensure_ascii=False)
    parser = argparse.ArgumentParser(description='Run model and generate report files  _roc.pdf, _cm.pdf, _report.csv, _tex ',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--ifile", type=str, default="data/TK.csv",
            help="input file: train_test_split will be run on this file (default: %(default)s)")

    parser.add_argument( "--model", type=str, default="GB",
            help="Model to test (default: %(default)s)")

    parser.add_argument("--overfit", action="store_true",
            help="overfit test: Use train data to predict outcome - ofile name will include _overfit_")

    parser.add_argument("--fit", action="store_true",
            help="fit model - otherwise load model from .pickle")

    parser.add_argument("--force", action="store_true",
            help="force overwrite of results")

    parser.add_argument("--showmodels", action="store_true",
            help="Show all models and exit")
    argv=parser.parse_args()
    if argv.showmodels:
        mymodel=mmodels.mmodels("GB").desc
        print(json.dumps(mymodel, indent=4, ensure_ascii=False))
        sys.exit(0)

    mfit=myfit(argv.fit,argv.model)
#    clf=mfit.fit_model(argv.fit)

    if argv.overfit:
        mfit.ofile=mfit.ofile+"_overfit"
        df=mfit.overfit_results()
    else:
        df=mfit.predict_results()

    res=mfit.ofile+"_res.csv"
    df.to_csv(res,index=False)
    print(f"results_file is {res}")
