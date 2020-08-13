#!/home/admin/anaconda3/bin/python3
#   author:martinmhan@yahoo.com date:  21/06/2020
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
#import joblib,argparse,re,sys,glob,os,time
import argparse,re,sys,glob,os,time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sklearn.metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from itertools import cycle
import json
import pprint
import myfit
import rpt2tex
import mmodels

class Treat4():
    """ Given input file and model name select the correct classifier.
    Compare results roc,cm,metrics with train/test split of data.
    Run trained model against TCE file to predict new planets.

    """
    def __init__(self,fit,model,overfit):
        """ 
        Given ifile and model name select the correct classifier name.
        Load classifier from pickle or generate new classifier
        train/test split of data.
        From fitted file create roc,cm and metrics
        From overfitted file create roc,cm and metrics

        """

        xfit=myfit.myfit(fit,model)
        self.ifile=xfit.ifile
        self.bTK=xfit.bTK
        ofile=xfit.ofile
        self.clf=xfit.clf

        print(f"ifile={self.ifile} ofile={ofile}xxx")
#        ofile="data/"+model # basename 

        self.df = pd.DataFrame()
        if overfit:
            self.rocfile=ofile+'_overfit_roc.pdf'
            self.cmfile=ofile+'_overfit_cm.pdf'
            self.metricfile=ofile+'_overfit_metric.csv'
            self.cref=ofile+"_overfit_cref.csv"
            self.df=xfit.overfit_results()
        else:
            self.rocfile=ofile+'_roc.pdf'
            self.cmfile=ofile+'_cm.pdf'
            self.metricfile=ofile+'_metric.csv'
            self.cref=ofile+"_cref.csv"
            self.df=xfit.predict_results()

        self.ifilepred=self.ifile.replace("TK", "TCE1") # Prediction file must already exist and have same extensions as TK... TCE1_...
        self.clftex=ofile+"_clf.tex" # Model same for fit/overfit

    def save_clf(self):    
        a=mmodels.mmodels(argv.model)
        output="\\begin{verbatim}\n\
                %s\n\
                \\end{verbatim}" %(a.clf)
#        clftex=self.ofile+"_clf.tex"
        with open(self.clftex,'w') as f: f.write(output)
        print(f"Saved Clf in {self.clftex}")

    # Merge data/KOI.csv and data/TCE.csv to data/TK.csv
    def getKepid(self,pfile,koi1):
        """ Generate Kepid. The KOI table contains kepid and kepoi_name (e.g. K00082.01)
        The TCE contains kepid and tce_plnt_num. This joins tables on kepid, tce_plnt_numb

        """
        for index, row in koi1.iterrows():
            #            koi1.loc[index,'tce_plnt_num'] = self.get_plnt_num(row['kepoi_name'])
            x=re.findall(r'\d$', row['kepoi_name']) # K00001.01 -> ['1']
            y=list(map(int, x)) # ['1'] -> 1 doesn't work?
            koi1.loc[index,'tce_plnt_num'] = int(y[0])

        koi1.tce_plnt_num = koi1.tce_plnt_num.astype(int) # ['1.0'] -> ['1']
        df=koi1.merge(pfile, indicator=True, how='outer')
        df=df.drop(['_merge'], axis=1)
        return df

    def plot_roc(self):
        """ Plot the ROC. If ifile and model begin with b it is binary not multiclass. """
        if self.bTK:
            style = {"CONFIRMED": "green","FALSE POSITIVE": "red"}
        else:
            style = {"CONFIRMED": "green","CANDIDATE": "darkorange","FALSE POSITIVE": "red"}

        plt.rcParams.update({'axes.labelsize': 'x-large'})
        fpr = dict();tpr = dict();roc_auc=dict();lw=2

        df=self.df.copy()
        for i in style:
            #    fpr[i], tpr[i],_ =roc_curve(y_test, df[i], pos_label=i)
            fpr[i], tpr[i],_ =roc_curve(df['y_test'], df[i], pos_label=i)
            roc_auc[i] = auc(fpr[i], tpr[i])
            plt.plot(fpr[i], tpr[i],color=style[i], lw=lw,\
                    label='AUC: {0} vs REST (area = {1:0.2f})'.format(i, roc_auc[i]))

            #y_score = clf.decision_function(X_test)
        # Plot ROC curve
        plt.plot([0, 1], [0, 1], 'k--')  # random predictions curve
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate or (1 - Specificity)')
        plt.ylabel('True Positive Rate or (Sensitivity)')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.savefig(self.rocfile)
        plt.clf()
        return self.rocfile

    def plot_cm(self):
        """ Plot the Confusion Matrix """
        # Confusion Matrix
        df=self.df.copy()
        cm = pd.crosstab(df.y_test, df.y_pred, rownames=['Actual'], colnames=['Predicted'])
        print(cm)
            #cm = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
        fig, (ax) = plt.subplots(1)
        sns.heatmap(cm,annot=True,cmap='Blues', fmt='g')

        # labels, title and ticks
        ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels');
        ax.set_title('Confusion Matrix');
        if self.bTK:
            ax.xaxis.set_ticklabels(['CONFIRMED', 'FALSE POSITIVE']);
        else:
            ax.xaxis.set_ticklabels(['CANDIDATE','CONFIRMED', 'FALSE POSITIVE']);
        print(f"plot cmfile {self.cmfile}")
        plt.savefig(self.cmfile)
        plt.clf()
        return self.cmfile

    def metric_csv(self,caption):
        " Generate latex reprot with roc,cm and metrics"""
        df=self.df.copy()
        print(sklearn.metrics.classification_report(df.y_test, df.y_pred,digits=3))
        report=sklearn.metrics.classification_report(df.y_test, df.y_pred,digits=3,output_dict=True)
        report = pd.DataFrame(report).transpose()
        report.to_csv(self.metricfile)
        print(f"write csvfile {self.metricfile}")
        return self.metricfile

    def div(self,x, y):
        """ If divsion by zero return 0 """
        return 0 if y == 0 else (x / y)*100

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run model and generate report files  _roc.pdf, _overfit_roc.pdf, _cm.pdf, _overfit_cm.pdf, _metric.csv, _tex ',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--model", type=str, default="GBtest",
            help="Model to test (default: %(default)s)")

    parser.add_argument("--fit", action="store_true",
            help="fit (and overfit)  model - otherwise load model from .pickle e.g. data/RF.pickle")

    parser.add_argument( "--caption", type=str, default="",
            help="Caption to add to eventual tex file (must be latex friendly) (default: %(default)s)")

    parser.add_argument("--showmodels", action="store_true",
            help="Show all models and exit")

    argv=parser.parse_args()

    if argv.showmodels:
        mymodel=mmodels.mmodels("GB").desc
        print(json.dumps(mymodel, indent=4, ensure_ascii=False))
#        pprint.pprint(mmodels.mmodels("GB").mycollection)
        sys.exit(0)

    if argv.fit: # Only fit model once then set to fit=false
        mytreat=Treat4(argv.fit,argv.model,overfit=False)
        argv.fit=False

# Run model on test data
    mytreat=Treat4(argv.fit,argv.model,overfit=False)
    froc=mytreat.plot_roc() 
    fcsv=mytreat.metric_csv(argv.caption)
    fcm=mytreat.plot_cm()
    del mytreat

# Overfit - run model on train data
    omytreat=Treat4(argv.fit,argv.model,overfit=True)
    ofroc=omytreat.plot_roc() 
    ofcm=omytreat.plot_cm()
    del omytreat

    caption=argv.caption
    myrpt=rpt2tex.rpt2tex(froc)
    modelname=argv.model.replace("_","")
    caption=f"{modelname}: Top Row: overfit test. Middle and bottom row test data"
    output=myrpt.ROCs(ofroc,ofcm,froc,fcm,fcsv,caption)
