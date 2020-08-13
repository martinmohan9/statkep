#!/home/admin/anaconda3/bin/python3
from datetime import datetime
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
import sklearn.utils
import pandas as pd
import argparse,sys
import json
import mmutils
import mmodels
import myfit
#import tpot.nn

# Class not needed
class Treat3():
    """ 
    Given a model this will launch tpot optimizer

    """
    def __init__(self,ifile):
        """
        The TCE file name is generated from the input file

        """
#        self.ifile=
        # Dummy values will
#        fit=False
#        xfit=myfit.myfit(fit,model)
#        self.ifile=xfit.ifile
#        self.bTK=xfit.bTK
#        ofile=xfit.ofile
#        self.model=model
        self.df=pd.read_csv(ifile,comment='#')
        self.y=self.df['koi_disposition'].reset_index(drop=True)
        self.X=self.df.drop(['kepid','koi_disposition','kepoi_name'], axis=1).reset_index(drop=True)
        self.df_train, self.df_test = train_test_split(self.df, test_size=0.1,random_state=42)
        self.df_train=self.df_train.reset_index(drop=True)
        self.df_test=self.df_test.reset_index(drop=True)
        self.X_train=self.df_train.drop(['kepid','koi_disposition','kepoi_name'], axis=1).to_numpy()
        self.y_train=self.df_train['koi_disposition']
        self.X_test=self.df_test.drop(['kepid','koi_disposition','kepoi_name'], axis=1).to_numpy()
        self.y_test=self.df_test['koi_disposition']

    def train_split(self):
#        df=pd.read_csv(self.ifile,comment='#')
#        df_train, df_test = train_test_split(df, test_size=0.1,random_state=42)
#        df_train=df_train.reset_index(drop=True)
#        df_test=df_test.reset_index(drop=True)
#        X_train=df_train.drop(['kepid','koi_disposition','kepoi_name'], axis=1).to_numpy()
#        y_train=df_train['koi_disposition']
#        X_test=df_test.drop(['kepid','koi_disposition','kepoi_name'], axis=1).to_numpy()
#        y_test=df_test['koi_disposition']
        return self.X_train,self.y_train,self.X_test,self.y_test

    def dur(self,starttime,endtime):
        diff = endtime - starttime
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        duration=(f"{hours}:{minutes}:{seconds}")
        #    total_mins = (diff.days*1440 + diff.seconds/60)
        return  (duration)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read input file and select Tpot model (Light,NN). Generate test/train data and run Tpot to find optimal model',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--ifile", type=str, default="data/TK.csv",
            help="Run tpot on ifile create train.csv,test.csv, Tpot.py (default: %(default)s)")

    parser.add_argument( "--model", type=str, default="None",
            help="Force Tpot model to choose a model.(Select None or Tpot_light to search for a model) (default: %(default)s)")

    parser.add_argument( "--generations", type=int, default="100",
            help="Number of generations  (default: %(default)s)")

    parser.add_argument( "--max_time_mins", type=int, default=None,
            help="Maximum time to run None for no max: (default: %(default)s)")

    parser.add_argument("--showmodels", action="store_true",
            help="Show all models and exit")

    argv=parser.parse_args()

    if argv.showmodels:
        mymodel=mmodels.mmodels("RF").desc
        print(json.dumps(mymodel, indent=4, ensure_ascii=False))
        print("--model config options for TPOT used in Treat3.py")
        print("None: Default: Searches all")
        print("Tpot_light: Used to find quick and simple pipelines")
        print("Tpot_nn: Used to find  neural networks")
#        print("Tpot_Gauss: Gaussian Model")
        sys.exit(0)

    random_state=42
    generations=argv.generations
    test_size=0.1
    config_dict=None
    model=argv.model
    early_stop=3
    ifile=argv.ifile
    max_time_mins=argv.max_time_mins

    mytreat=Treat3(argv.ifile)

    if argv.model=="None": config_dict=None
    elif argv.model=="Tpot_light": config_dict="TPOT light"
#    elif argv.model=="Tpot_nn": config_dict= {'tpot.nn.PytorchLRClassifier': {}}
    elif argv.model=="Tpot_nn": config_dict="TPOT NN"
    elif argv.model=="Tpot_Gauss": 
        config_dict= {
            'sklearn.naive_bayes.GaussianNB': {
                },
            'sklearn.naive_bayes.BernoulliNB': {
                'alpha': [1e-3, 1e-2, 1e-1, 1., 10., 100.],
                'fit_prior': [True, False]
                },
            'sklearn.naive_bayes.MultinomialNB': {
                'alpha': [1e-3, 1e-2, 1e-1, 1., 10., 100.],
                'fit_prior': [True, False]
                }
            }
    else: 
        config_dict="TBD" # To Be Decided
    # Doesn't supply any significant results

    if config_dict=="TBD": # Set config_dict
        mymodel=mmodels.mmodels(argv.model)
        models=mymodel.config # GB -> sklearn.ensemble.GradientBoostingClassifier
        key=models[argv.model]
        value="{{ }}"
        config_dict={key:{}}

    df = pd.read_csv(ifile,comment= '#')
    
# Need to factorize
    X_train,y_train,X_test,y_test=mytreat.train_split()
    y_test, uniques =pd.factorize(y_test,sort=False)
    y_train, uniques =pd.factorize(y_train,sort=False)

    starttime=datetime.now()

    # Configure
    tpotConf=f"# TPOTClassifier(verbosity=2,generations={generations},config_dict={config_dict},max_time_mins={max_time_mins},random_state={random_state},early_stop={early_stop})"
    print(tpotConf)
    Tpot = TPOTClassifier(verbosity=2,generations=generations,config_dict=config_dict,max_time_mins=max_time_mins,random_state=random_state,early_stop=early_stop)
    Tpot_file=ifile.replace(".csv","_"+str(generations)+"g_"+model+"_Tpot.py")
    print(f"Fitting to file {Tpot_file}")

    # Start
    Tpot.fit(X_train, y_train)
    Tpot_score=Tpot.score(X_test, y_test)
    Tpot.export(Tpot_file)
    print(f"Score see {Tpot_file}") # The correct score is in the tpot export file
    endtime=datetime.now()
    duration=mytreat.dur(starttime,endtime)

    mycomments=tpotConf
    mycomments=mycomments+f'# ifile {ifile}  model={argv.model} Tpot_file={Tpot_file}, Tpot_score={Tpot_score}, starttime{starttime}, endtime={endtime} duration={duration}\n'
    myutils=mmutils.mmutils()
    myutils.prependComments(Tpot_file,mycomments)
