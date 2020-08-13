import re,glob,os
import rpt2tex
class mmutils():
    """ Utilities for writing. """
    def __init__(self):
        pass

    # prepend comments to csv - should be last fn called before closing
    def prependComments(self,filename,comments):
        with open(filename,'r') as contents:
            save = contents.read()
        with open(filename,'w') as contents:
            contents.write(comments)
        with open(filename,'a') as contents:
            contents.write(save)
        return comments

    def write2tex(self,ifile,caption,ofile,force=False):
        t1=ofile+".tex"
        t2=ofile+"_rpt.tex"
        f1 = glob.glob(t1)
        f2 = glob.glob(t2)
        myrpt=rpt2tex.rpt2tex(ifile)
        if (force):
            myrpt.roctex(caption)
            print(f'Saved {f1} {f2}')
        elif (f1 or f2):
            print(f'WARNING: {ifile} {caption} not executed to create ofile*tex {f1} or {f2} exist !')
        else:
            myrpt.roctex(caption)
            print(f'Saved {f1} {f2}')
    
    def write2plt(self,plt,fname,force=False):
        f1 = glob.glob(fname)
        if (force):
            plt.savefig(fname)
            print(f'Saved {fname}')
        elif f1:
            print(f'WARNING: {fname} not created because it exists!')
        else:
            plt.savefig(fname)
            print(f'Saved {fname}')
    
    def write2csv(self,df,fname,force=False):
        f1 = glob.glob(fname)
        if (force):
            df.to_csv(fname)
            print(f'Saved {fname}')
        elif f1:
            print(f'WARNING: {fname} not created because it exists!')
        else:
            df.to_csv(fname)
            print(f'Saved {fname}')
    
