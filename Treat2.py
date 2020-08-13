#!/home/admin/anaconda3/bin/python3
#   author:martinmhan@yahoo.com date:  17/06/2020
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
from datetime import datetime
import pandas as pd
import numpy as np
import argparse,sys,re
import matplotlib.pyplot as plt
import seaborn; seaborn.set()
#import mmutils
import myfit
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from shutil import copyfile
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

class Treat2():
    """ 
    This class will modify the input file depending on the user selection.
    After modification name of the output file is modifed to reflect the change.
    e.g. if outlier removal applied ifile.csv -> ifile_out.csv
    Only one method can be called at time.
    The TCE file is modified the same way as the TK file

    """
    def __init__(self,ifile):
        """
        The input file is saved

        """
        self.ifile=ifile
        self.TCE1=self.ifile.replace("TK","TCE1")

    def bin(self): # Merge FP and CANDIDATE - all files contain b at start
        self.TK=self.ifile
        bTK=self.TK.replace("data/", "data/b")
        df = pd.read_csv(self.TK,comment= '#')
        df["koi_disposition"] = df["koi_disposition"].replace(to_replace="CANDIDATE",value="FALSE POSITIVE")
        df.to_csv(bTK,index=False)
        print(f"Created {bTK}")

        # Just rename TCE1 to bTCE1 it has no koi_disposition
        TCE1=self.TK.replace("TK","TCE1")
        bTCE1=TCE1.replace("data/", "data/b")
#        bTCE1=bTK.replace("TK", "TCE1")
#        df = pd.read_csv(TCE1,comment= '#') 
#        df.to_csv(bTCE1,index=False)
        copyfile(TCE1, bTCE1)
        print(f"Copy {TCE1} to {bTCE1} (no koi_dispostion)")

    def get_vif(self,exogs, data): # This needs to be done iteratively
        ''' 
        From https://stackoverflow.com/questions/42658379/variance-inflation-factor-in-python
        Return VIF (variance inflation factor) DataFrame

        Args:
        exogs (list): list of exogenous/independent variables
        data (DataFrame): the df storing all variables

        Returns:
        VIF and Tolerance DataFrame for each exogenous variable

        Notes:
        Assume we have a list of exogenous variable [X1, X2, X3, X4].
        To calculate the VIF and Tolerance for each variable, we regress
        each of them against other exogenous variables. For instance, the
        regression model for X3 is defined as:
                        X3 ~ X1 + X2 + X4
        And then we extract the R-squared from the model to calculate:
                    VIF = 1 / (1 - R-squared)
                    Tolerance = 1 - R-squared
        The cutoff to detect multicollinearity:
                    VIF > 10 or Tolerance < 0.1
        '''

        # initialize dictionaries
        vif_dict, tolerance_dict = {}, {}
        # create formula for each exogenous variable
        for exog in exogs:
            not_exog = [i for i in exogs if i != exog]
            formula = f"{exog} ~ {' + '.join(not_exog)}"
            # extract r-squared from the fit
            r_squared = smf.ols(formula, data=data).fit().rsquared

            # calculate VIF
            vif = 1/(1 - r_squared)
            vif_dict[exog] = vif

            # calculate tolerance
            tolerance = 1 - r_squared
            tolerance_dict[exog] = tolerance
        # return VIF DataFrame
        df_vif = pd.DataFrame({'VIF': vif_dict, 'Tolerance': tolerance_dict})
        return df_vif 

    def cap2(self):
        # Cap columns which are not commented out
        cap_cols=[
                'tce_period',
                'tce_time0bk',
                'tce_time0',
                'tce_ror',
                'tce_dor',
                'tce_incl',
                'tce_impact',
                'tce_duration',
                'tce_ingress',
                'tce_depth',
                'tce_ldm_coeff1',
                'tce_ldm_coeff2',
                'tce_ldm_coeff3',
                'tce_ldm_coeff4',
                'tce_full_conv',
                'tce_model_snr',
                'tce_model_chisq',
                'tce_model_dof',
                'tce_robstat',
                'tce_dof1',
                'tce_dof2',
                'tce_chisq1',
                'tce_chisq2',
                'tce_chisqgofdof',
                'tce_chisqgof',
                'tce_prad',
                'tce_sma',
                'tce_eqt',
                'tce_insol',
                'tce_steff',
                'tce_slogg',
                'tce_smet',
                'tce_sradius',
                'tce_smet_prov',
                'tcet_period',
                'tcet_time0bk',
                'tcet_time0',
                'tcet_duration',
                'tcet_ingress',
                'tcet_depth',
                'tcet_model_chisq',
                'tcet_model_dof',
                'wst_robstat',
                'wst_depth',
                'tce_mesmedian',
                'tce_mesmad',
                'tce_maxmes',
                'tce_minmes',
                'tce_maxmesd',
                'tce_minmesd',
        'tce_max_sngle_ev',
         'tce_max_mult_ev',
         'tce_bin_oedp_stat',
         'tce_rmesmad',
         'tce_rsnrmes',
         'tce_rminmes',
         'tce_albedo',
         'tce_ptemp',
         'tce_albedo_stat',
         'tce_ptemp_stat',
         'boot_fap',
         'boot_mesthresh',
         'boot_mesmean',
         'boot_messtd',
         'tce_cap_stat',
         'tce_hap_stat',
         'tce_rb_tpdur',
         'tce_rb_tcount0',
         'tce_rb_tcount1',
         'tce_rb_tcount2',
         'tce_rb_tcount3',
         'tce_rb_tcount4',
         'tce_fwm_stat',
         'tce_fwm_sra',
         'tce_fwm_sdec',
         'tce_fwm_srao',
         'tce_fwm_sdeco',
         'tce_fwm_prao',
         'tce_fwm_pdeco',
         'tce_dicco_mra',
         'tce_dicco_mdec',
         'tce_dicco_msky',
         'tce_dikco_mra',
         'tce_dikco_mdec',
         'tce_dikco_msky',
         'tce_period_sn',
         'tce_time0bk_sn',
         'tce_time0_sn',
         'tce_ror_sn',
         'tce_dor_sn',
         'tce_incl_sn',
         'tce_impact_sn',
         'tce_duration_sn',
         'tce_ingress_sn',
         'tce_depth_sn',
         'tce_prad_sn',
         'tce_sma_sn',
         'tce_eqt_sn',
         'tce_insol_sn',
         'tce_steff_sn',
         'tce_slogg_sn',
         'tce_smet_sn',
         'tce_sradius_sn',
         'tce_albedo_sn',
         'tce_ptemp_sn',
         'tce_fwm_sra_sn',
         'tce_fwm_sdec_sn',
         'tce_fwm_srao_sn',
         'tce_fwm_sdeco_sn',
         'tce_fwm_prao_sn',
         'tce_fwm_pdeco_sn',
         'tce_dicco_mra_sn',
         'tce_dicco_mdec_sn',
         'tce_dicco_msky_sn',
         'tce_dikco_mra_sn',
         'tce_dikco_mdec_sn',
         'tce_dikco_msky_sn'
         ]
        df = pd.read_csv(self.ifile,comment= '#')
        X= df[df.columns & cap_cols] # Only copy existing cols
        dfcap=X.apply(self.capOutliers) # Apply to df
        dfrest=df.drop(cap_cols, axis=1,errors='ignore') # The rest
        dfnew = pd.concat([dfrest.reset_index(drop=True), dfcap], axis=1)

        ofile=self.ifile.replace(".csv", "_cap2.csv")       
        dfnew.to_csv(ofile,index=False)
        print(f"{self.ifile} {df.shape} to {ofile} {dfnew.shape}")

    def cap1(self):
        # Cap columns which are not commented out
        cap_cols=[
                # 'tce_period',
                # 'tce_time0bk',
                # 'tce_time0',
                # 'tce_ror',
                # 'tce_dor',
                'tce_incl',
                'tce_impact',
                'tce_duration',
                'tce_ingress',
                # 'tce_depth',
                'tce_ldm_coeff1',
                'tce_ldm_coeff2',
                'tce_ldm_coeff3',
                'tce_ldm_coeff4',
                # 'tce_full_conv',
                # 'tce_model_snr',
                'tce_model_chisq',
                'tce_model_dof',
                # 'tce_robstat',
                'tce_dof1',
                # 'tce_dof2',
                # 'tce_chisq1',
                # 'tce_chisq2',
                'tce_chisqgofdof',
                # 'tce_chisqgof',
                # 'tce_prad',
                # 'tce_sma',
                'tce_eqt',
                # 'tce_insol',
                'tce_steff',
                'tce_slogg',
                'tce_smet',
                # 'tce_sradius',
                'tce_smet_prov',
                # 'tcet_period',
                # 'tcet_time0bk',
                # 'tcet_time0',
                'tcet_duration',
                'tcet_ingress',
                # 'tcet_depth',
                # 'tcet_model_chisq',
                # 'tcet_model_dof',
                # 'wst_robstat',
                # 'wst_depth',
                # 'tce_mesmedian',
                # 'tce_mesmad',
                # 'tce_maxmes',
                'tce_minmes',
                'tce_maxmesd',
                # 'tce_minmesd',
        # 'tce_max_sngle_ev',
        # 'tce_max_mult_ev',
         'tce_bin_oedp_stat',
        # 'tce_rmesmad',
         'tce_rsnrmes',
         'tce_rminmes',
        # 'tce_albedo',
         'tce_ptemp',
         'tce_albedo_stat',
         'tce_ptemp_stat',
         'boot_fap',
         'boot_mesthresh',
         'boot_mesmean',
         'boot_messtd',
        # 'tce_cap_stat',
        # 'tce_hap_stat',
         'tce_rb_tpdur',
        # 'tce_rb_tcount0',
        # 'tce_rb_tcount1',
        # 'tce_rb_tcount2',
        # 'tce_rb_tcount3',
        # 'tce_rb_tcount4',
        # 'tce_fwm_stat',
         'tce_fwm_sra',
         'tce_fwm_sdec',
        # 'tce_fwm_srao',
        # 'tce_fwm_sdeco',
        # 'tce_fwm_prao',
        # 'tce_fwm_pdeco',
        # 'tce_dicco_mra',
        # 'tce_dicco_mdec',
        # 'tce_dicco_msky',
        # 'tce_dikco_mra',
        # 'tce_dikco_mdec',
        # 'tce_dikco_msky',
        # 'tce_period_sn',
        # 'tce_time0bk_sn',
        # 'tce_time0_sn',
        # 'tce_ror_sn',
        # 'tce_dor_sn',
        # 'tce_incl_sn',
        # 'tce_impact_sn',
        # 'tce_duration_sn',
        # 'tce_ingress_sn',
        # 'tce_depth_sn',
         'tce_prad_sn',
         'tce_sma_sn',
         'tce_eqt_sn',
         'tce_insol_sn',
         'tce_steff_sn',
         'tce_slogg_sn',
         'tce_smet_sn',
         'tce_sradius_sn',
         'tce_albedo_sn',
         'tce_ptemp_sn',
         #'tce_fwm_sra_sn',
         #'tce_fwm_sdec_sn',
         'tce_fwm_srao_sn',
         'tce_fwm_sdeco_sn',
         'tce_fwm_prao_sn',
         'tce_fwm_pdeco_sn',
         'tce_dicco_mra_sn',
         'tce_dicco_mdec_sn',
         #'tce_dicco_msky_sn',
         'tce_dikco_mra_sn',
         'tce_dikco_mdec_sn',
         #'tce_dikco_msky_sn'
         ]
        df = pd.read_csv(self.ifile,comment= '#')
        X= df[df.columns & cap_cols] # Only copy existing cols
        dfcap=X.apply(self.capOutliers) # Apply to df
        dfrest=df.drop(cap_cols, axis=1,errors='ignore') # The rest
        dfnew = pd.concat([dfrest.reset_index(drop=True), dfcap], axis=1)

        ofile=self.ifile.replace(".csv", "_cap1.csv")       
        dfnew.to_csv(ofile,index=False)
        print(f"{self.ifile} {df.shape} to {ofile} {dfnew.shape}")

    def capOutliers(self,iv):
        ''' Cap all outliers Interquartile range IQR*1.5 '''        
        outlierConstant=3
        a = np.array(iv)
        upper_quartile = np.percentile(a, 75)
        lower_quartile = np.percentile(a, 25)

        IQR = (upper_quartile - lower_quartile) * outlierConstant
        quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
        resultList = []
        for y in a.tolist():
            #            if y >= quartileSet[0] and y <= quartileSet[1]:
#                resultList.append(y)
# Cap outliers
            if y <= quartileSet[0]:
                resultList.append(quartileSet[0])
            elif y >= quartileSet[1]:
                resultList.append(quartileSet[1])
            else: 
                resultList.append(y)
        noCap=a
        Cap=resultList
        return Cap

    def pca(self):
        cols=['kepid','tce_plnt_num','koi_disposition','kepoi_name']
        df=pd.read_csv(self.ifile,comment= '#')
        df=df.copy()

        dfsave=df[df.columns & cols].copy() # Save index cols for later
        X=df.drop(cols, axis=1,errors='ignore') # Get X values for pca

        pca=PCA(n_components=0.95)
        dfsave['pca']=pca.fit_transform(X) #  Add pca'd cols

        ofile=self.ifile.replace(".csv", "_pca.csv")       
        dfsave.to_csv(ofile,index=False)
        print(f"{self.ifile} to {ofile} with col 'pca' var ={pca.explained_variance_ratio_} {pca.singular_values_}")

    def vif(self):
        """ A list of highly correlate IV's (VIF>10) removed iteratively
        usign get_vif. """

        cols=['tce_period','tce_eqt_sn','tcet_time0bk','boot_messtd','tcet_time0',\
                'tce_ldm_coeff3','tce_dof1','tce_time0bk_sn','tce_max_mult_ev',\
                'tce_time0','tce_smet_prov','tce_ldm_coeff2',\
                'tce_rb_tcount0','tce_maxmes','tce_sma','tce_fwm_sra_sn',\
                'tcet_duration','tce_chisqgofdof','tce_robstat','wst_robstat',\
                'tce_period_sn','tce_smet','tce_depth','tce_dicco_mdec_sn']

        df=pd.read_csv(self.ifile,comment= '#') 
        dfvif=df.drop(cols, axis=1)
        vifFile=self.ifile.replace(".csv","_vif.csv")   
        dfvif.to_csv(vifFile,index=False)
        print(f"{self.ifile} {df.shape} to {vifFile} {dfvif.shape}")

if __name__ == '__main__':
    """ The _main__ models is used for testing"""

    parser = argparse.ArgumentParser(description=" Read files data/TK.csv and data/TCE1.csv created by Treat1.py. Create new file depending on options e.g --b bTK.csv - Use Treat2.sh to call this",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--ifile", type=str, default="data/TK.csv",
            help="input file (default: %(default)s)")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("--bin", action="store_true",
            help="koi_disposition (DV): Create CONFIRMED vs REST file TK=>bTK (i.e merge CANDIDATE with FALSE POSITIVE n.b this alos creates data/bTCE.csv)")
    group.add_argument("--cap1", action="store_true",
            help="Cap _selected_ outliers (.75pcntile - .25pcntile) which are not categorical")

    group.add_argument("--cap2", action="store_true",
            help="Cap _all_ outliers (.75pcntile - .25pcntile) which are not categorical")

    group.add_argument("--pca", action="store_true",
            help="Product Component Analysis (pc)")

    group.add_argument("--vif", action="store_true",
            help="Remove multicorrelatd ivs and save _vif")
    argv=parser.parse_args()

#    class Args:
#        cap = False
#        bin = False
#        pca = False
#        vif = True
#        TK="data/TK.csv"
#        TCE1="data/TCE1.csv"
#        model="GB"
#    argv=Args()
    df = pd.read_csv(argv.ifile,comment= '#')

    mytreat=Treat2(argv.ifile)

    if(argv.bin): # No effect on TCE1 which does not have koi_disposition
        mytreat.bin()
    elif(argv.cap1): 
        mytreat.cap1()
    elif(argv.cap2):
        mytreat.cap2()
    elif(argv.pca):
        mytreat.pca() 
#    elif(argv.npca):
#        mytreat.npca()  # Standardized first
    elif(argv.vif):
        mytreat.vif()
    else: 
        print("Unknown argument")
