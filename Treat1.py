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
import pandas as pd
import numpy as np
import argparse,sys,re
from sklearn.impute import SimpleImputer

class Treat1():
    """ 
    This takes two files download from NASA.
    TCE.csv: https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=tce
    KOI.csv: https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=koi

    TCE.csv (34,000+ cases) is cleaned and saved as TCE1.csv (34,000+ cases)
    TCE.scv (34,000+ cases) is merged with corresponding lines in KOI.csv (8,000+ cases) and saved  as TK.csv(8,000+ cases)

    """
    def __init__(self,TCE="data/TCE.csv",KOI="data/KOI.csv"):
        """
        The TCE file name is generated from the input file

        """
        self.TCE=TCE
        self.KOI=KOI
        self.TK="data/TK.csv"
        self.TCE1="data/TCE1.csv"

    global mycomments
    dropCols=[]

    # Global mycomments
    mycomments=f"# Merge KOI.csv and TCE.csv, drop cols, impute missing data\n"

    def eprint(self,*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def getComments(self,Fname):
        comments=[]
        with open(Fname) as rows: # Get comments from csv
            for line in rows:
                if line.startswith("# COLUMN"):
                    comments.append(line.strip())
        return comments

    # prepend comments to csv - should be last fn called before closing
    def prependComments(self,filename,comments):
        print(comments)
        with open(filename,'r') as contents:
            save = contents.read()
        with open(filename,'w') as contents:
            contents.write(comments)
        with open(filename,'a') as contents:
            contents.write(save)
        return comments

    def getDescription(self,col):
        """ Extracts NASA COMMENT from TCE.csv -> retun col,description. """
        # Find col description
        comment2=col+",No description"
        for comment in comments: # comment associated with col from TCE.csv
            if (col+":") in comment:
                comment2=re.sub(r'\#.*?COLUMN ', '', comment)
                comment2=re.sub(r':\s+', ',', comment2)
    #            eprint(comment2)
        return comment2

    def imputeMostFreq(self,df): 
        """ For missing values impute most frequent """
        global mycomments
        df.columns[df.isnull().any()]
        temp=df.columns[df.isnull().any()]
        temp=str(temp)
        temp = temp.replace('\r', '').replace('\n', '')
        mycomments=mycomments+f"# imputeMostFreq for cols {temp}\n"
        fill_NaN = SimpleImputer(missing_values=np.nan, strategy="most_frequent") # Works with strings
        imputed_DF = pd.DataFrame(fill_NaN.fit_transform(df))
        imputed_DF.columns = df.columns
        imputed_DF.index = df.index
        df=imputed_DF
        return df

    def dropRogues(self,df): 
        """ Rogue flag indicates less than 3 transits and should have been droppe but it still occurs """
        global mycomments
        nr_rogues=df[df['tce_rogue_flag']==1].shape[0]
        df2=df.query('tce_rogue_flag == 0').copy()
        df2.drop(columns=['tce_rogue_flag'],inplace=True) # Don't drop col otherwiset model complains that col numbers are different
        mycomments=mycomments+f"# dropRogues: {nr_rogues} rogues rows {df2.shape[0]},cols {df2.shape[1]}\n"
    #    eprint("dropRogues: %d rogues rows %d,cols %d" %(nr_rogues,df2.shape[0],df2.shape[1]))
        return df2

    def errToSNR(self,df):
        """ Err signal by itself makes no sense so modify _err to _sn by getting  e.g. tce_period_sn=tce_period/tce_period_err. """
        cols=["tce_period", "tce_time0bk", "tce_time0", "tce_ror", "tce_dor", "tce_incl", "tce_impact", "tce_duration", "tce_ingress", "tce_depth", "tce_prad", "tce_sma", "tce_eqt", "tce_insol", "tce_steff", "tce_slogg", "tce_smet", "tce_sradius", "tce_albedo", "tce_ptemp", "tce_fwm_sra", "tce_fwm_sdec", "tce_fwm_srao", "tce_fwm_sdeco", "tce_fwm_prao", "tce_fwm_pdeco", "tce_dicco_mra", "tce_dicco_mdec", "tce_dicco_msky", "tce_dikco_mra", "tce_dikco_mdec", "tce_dikco_msky"]
        # Drop _err values
        for col in cols:
            err=col+"_err"
            comment=self.getDescription(err)
            print("%s,modify _err,_err to _sn" %(comment))

        for col in cols:
            err=col+"_err"
            sn=col+"_sn"

            if col not in df: 
                df[sn]=0 # col does not exist set to 0
            else:
                df[sn]=df[col].div(df[err])

            if col in df.columns:
                df[sn] = df[sn].replace([np.inf,-np.inf],0)
                df.drop(columns=[err],inplace=True)
        return df

    def dataframe_difference(self,df1, df2, which=None, fname='diff.csv'):
        """ Find rows which are different between two DataFrames."""
        comparison_df = df1.merge(df2, indicator=True, how='outer')
        diff_df = comparison_df[comparison_df['_merge'] == which]

        diff_df.to_csv(fname,index=False)
        return diff_df

    # Extract K00082.01 -$>$ ['1']
    def get_plnt_num(self,kepname):
        """ Extract planet number from kepler string and use this for merges """
        x=re.findall(r'\d$', kepname) # K00001.01 -> ['1']
        y=list(map(int, x)) # ['1'] -> 1 doesn't work?
        return int(y[0])


    def mergeTceKoi(self):
        """ Merge data/KOI.csv and data/TCE.csv to data/TK.csv. """
        global mycomments
    #    diff_file="data/diff_file.csv"
    #    merge_file="data/merge_file.csv"
        tce = pd.read_csv(self.TCE,comment= '#')
        koi = pd.read_csv(self.KOI,comment= '#')
        mycomments=mycomments+f"# mergeTceKoi: self.TCE: {self.TCE} rows {tce.shape[0]},cols {tce.shape[1]}\n"
        mycomments=mycomments+f"# mergeTceKoi: self.KOI: {self.KOI} rows {koi.shape[0]},cols {koi.shape[1]}\n"
        # Get koi's cols you want to merge
        koi1 = koi[['kepid', 'kepoi_name','koi_disposition']].copy()
         # Get all cols from koi just set koi1 = koi

        # Extract plnt_num: kepoi_name ['K00082.01'] -> plnt_num ['1.0']
        for index, row in koi1.iterrows():
            koi1.loc[index,'tce_plnt_num'] = self.get_plnt_num(row['kepoi_name'])
        # Float to int i.e. ['1.0'] -> tce_plnt_num ['1']
        koi1.tce_plnt_num = koi1.tce_plnt_num.astype(int)

        # File difference
        comparison_df= koi1.merge(tce, indicator=True, how='outer')
        df = comparison_df[comparison_df['_merge'] == "left_only"]

        # Merge file
        comparison_df= koi1.merge(tce, indicator=True, how='outer')
        df = comparison_df[comparison_df['_merge'] == "both"]
        mycomments=mycomments+f"# mergeTceKoi: out rows {df.shape[0]},cols {df.shape[1]}\n"
        return df

    def dropNunique(self,df):
        """ Drop columns which are not unique and have no predictive possibilities """
        global mycomments
        global dropCols
        dfpre=df.shape[1]
    #    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    #    print("dropNunique: Dropped %d ^Unnamed cols: (rows %d,cols %d) " %(dfpre-df.shape[1],df.shape[0],df.shape[1]))

        nunique = df.apply(pd.Series.nunique,dropna=False)
        cols_to_drop = nunique[nunique == 1].index
        for col in cols_to_drop:
            comment=self.getDescription(col)
    #        if(bool(re.match(r'^av_', col))):
            if(re.match(r'^av_', col)):
                print("%s,empty entries,Drop" %(comment))
            else:
                print("%s,identical entries,Drop" %(comment))

        dfpre=df.shape[1]
        df.drop(cols_to_drop, axis=1,inplace=True)
        print("dropNunique: cols_dropped {cols_to_drop}")

        # Factorize cols
        clist=['tce_steff_prov','tce_slogg_prov','tce_smet_prov','tce_sradius_prov']
        for c in clist:
            if c in df.columns:
                df[c],uniques=pd.factorize(df[c])
                print("%s,Factorize,Fact" %self.getDescription(c))

        mycomments=mycomments+f"# dropNunique: out rows {df.shape[0]}, cols {df.shape[1]}\n"
    #    eprint("dropNunique: out rows %d,cols %d" %(df.shape[0],df.shape[1]))
        return df

    def dropMan(self,df): # Select cols to drop manually
        """ These wre selected manually for dropping as they have no predictive qualities """
        global mycomments
        # Dict key: Manual cols to drop reason added manually
        dcols = {
                #"kepid": "Will be needed to identify planets in future",
                #        "kepoi_name":"not needed", 
                "rowid": "not needed",
                "tce_longp_err": "tce_longp non-existent",
                "tce_eccen_err": "tce_longp non-existent",
                "tce_datalink_dvs":"pdf file",
                "tce_datalink_dvr":"pdf file",
                #        "tce_quarters":"A string of seventeen zeroes and ones indicating which quarters contain data"
                }

        for d in dcols:
            if d in df.columns:
                df.drop(columns=[d],inplace=True)
                comment=self.getDescription(d)
                print("%s,%s,mDrop" %(comment,dcols[d]))

        # Dict key: Additional info from website
        dcols = {
                "tce_quarters":"A string of seventeen zeroes and ones indicating which quarters contain data"
                }
        for d in dcols:
            if d in df.columns:
                df.drop(columns=[d],inplace=True) # kepoi_name no longer needed
                comment=self.getDescription(d)
                print("%s %s,See \\textsuperscript{\\ref{foot:tce_desc}},mDrop" %(comment,dcols[d]))
    #    eprint("dropMan: out rows %d,cols %d" %(df.shape[0],df.shape[1]))
        mycomments=mycomments+f"# dropMan: out rows {df.shape[0]}, cols {df.shape[1]}\n"
        return df

    def cleanAll(self,df): # Select cols to drop manually
        """ More cols to drop manually """
        global mycomments
        df=mytreat.dropNunique(df)
        #mycomments=mycomments+f"# koi_disposition(DV): CONFIRMED,CANDIDATE,FALSE POSITIVE\n"
        df=mytreat.dropMan(df) # Select cols to drop manually
        df=mytreat.dropRogues(df)
        df=mytreat.errToSNR(df) # Convert error signal to sn signal
        #mycomments=mycomments+f"# errToSNR performed\n"
        df=(self.imputeMostFreq(df)) # most frequent imputation

        cols=['tce_delivname', 'rowupdate', 'tce_eccen', 'tce_longp',\
                'tce_limbdark_mod', 'tce_trans_mod', 'tce_ioflag', 'tcet_period_err',\
                'tcet_time0bk_err', 'tcet_time0_err', 'tcet_duration_err',\
                'tcet_ingress_err', 'tcet_depth_err', 'tcet_full_conv', 'av_vf_pc',\
                'av_vf_pc_err', 'av_vf_afp', 'av_vf_afp_err', 'av_vf_ntp',\
                'av_vf_ntp_err', 'av_pp_pc', 'av_pp_afp', 'av_pp_ntp',\
                'av_training_set', 'av_pred_class', '_merge']
        mycomments=mycomments+f"# Force drop {cols}\n"
        df=df.drop(cols, axis=1, errors='ignore')
    #    df.to_csv(ofile,index=False)
        return df

if __name__ == '__main__':
    """ The _main__ models is used for testing"""
    parser = argparse.ArgumentParser(description="1. TCE.csv impute data, drop cols, drop rogue flags 'TCE1.csv' then merge data/KOI.csv (koi_dispostion,kepoi_name) -> 'TK.csv' - This is only run once at start ",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--tcefile", type=str, default="data/TCE.csv",
            help="tce file contains all the IV's (default: %(default)s)")

    parser.add_argument( "--koifile", type=str, default="data/KOI.csv",
            help="koi file used to obtain DV (default: %(default)s)")

    argv=parser.parse_args()
    mytreat=Treat1(argv.tcefile,argv.koifile)

    # Extract original comments from data/TCE.csv
    comments=mytreat.getComments(mytreat.TCE)
    print("Name,Description,Reason,Treat")

    predF=mytreat.TCE1
    df = pd.read_csv(mytreat.TCE,comment= '#')
    df = mytreat.cleanAll(df)
    df.to_csv(predF,index=False)
    com=f"# TCE File {predF} rows {df.shape[0]} cols {df.shape[1]}\n"
#    mytreat.eprint(com)
    mycomments=mycomments+com
    mytreat.prependComments(predF,mycomments)

    mergeF=mytreat.TK
    df=mytreat.mergeTceKoi()
    df = mytreat.cleanAll(df)
    df.to_csv(mergeF,index=False) # Test File TCE1.csv
    com=f"# TK File {mergeF} rows {df.shape[0]} cols {df.shape[1]}\n"
#    mytreat.eprint(com)
    mycomments=mycomments+com
    mytreat.prependComments(mergeF,mycomments)
