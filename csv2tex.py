#!/usr/bin/env python
# coding: utf-8
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

import pandas as pd
import argparse,re,os

class csv2tex():
    def __init__(self,ifile):
        self.ifile=ifile
        self.df = pd.read_csv(self.ifile,comment= '#')
#        self.ofile=re.sub('.csv', '.tex', self.ifile) # csv to tex 
        self.ofile=self.ifile.replace('.csv', '.tex') # csv to tex 

    def create_tex(self,caption):

        #        output=self.create_tex(cap)
        rows,cols=self.df.shape[0],self.df.shape[1]
        tabname=self.generatetab()
#        caption="" # disabled

        if caption:
            header="\\begin{table}[!htbp]\n \\centering\n \\caption{%s}\n \\label{%s} \n  \\begin{tabular}\n{| \n" %(caption,tabname)
        else:
            header="\\expandafter\\newcommand\\csname %s\\endcsname{\n\\begin{table}[H]\n\\begin{tabular}\n{| \n" %tabname

        colwidth=""
        colsize=str(round(1/cols,3))
        for i in range(cols):
            colwidth=colwidth+' p{\\dimexpr'+colsize+'\\textwidth-2\\tabcolsep-\\arrayrulewidth\\relax}| \n'
        colwidth=colwidth+"}\hline \n"

        df=self.df.rename(columns={"Unnamed: 0": ""})
        row1=df.columns
        lrow1=""
        for i in (row1):
            lrow1=lrow1+"\\textbf{"+i+"} &"
        lrow1=re.sub('\&$', '', lrow1) # remove last &

        lrow1=lrow1+"\\\\ \hline \n"

#        rows=pd.read_csv(self.ifile)
        rows=self.df
        lbody=""
        for index, row in rows.iterrows():
            lrow=""
            for r in row:
                if type(r) != str : r=str(round(r, 3)) # Convert to string if nr
                # some escapes
                r=re.sub('&','\\&', r)
                r=re.sub('<','$<$', r)
                r=re.sub('>','$>$', r)

                lrow=lrow+str(r)+" &"
            lbody=lbody+lrow
            lbody=re.sub('\&$', '', lbody) # remove last &
            lbody=lbody+"\\\\ \hline \n"

        if caption:
            tail="\\end{tabular} \n\end{table}"
        else:
            tail="\\end{tabular} \n\end{table}\n}"
#        tail="\\end{tabular} \n\end{table}\n}"

    #header="\\begin{table}[!htbp]\n \\centering\n \\caption{"+self.ifile+": rows "+str(rows)+" cols "+str(cols)+"}\n \\label{tbl:"+self.ifile+"} \n  \\begin{tabular}\n{| \n"
        rows,cols=df.shape[0],df.shape[1]
    #tail="\\end{tabular}\n\\centering\n\\caption{"+self.ifile+": rows "+str(rows)+" cols "+str(cols)+"}\n\\label{tbl:"+self.ifile+"}\n\\end{table}"

        output=header+colwidth+lrow1+lbody+tail
        output=re.sub('_', '\\_', output) # csv to ltx

        with open(self.ofile,'w') as f: f.write(output)
        print(f"csv2tex: {self.ifile} -> {self.ofile}")
        return output
    #print(output)

# If latex \newcommand{tabname}  contains nr (1,2...) latex will not compile
# Need to add endscape
    def generatetab(self):
        nrs = []
        nrs=re.findall(r'\d+', self.ifile)
        tabname=self.ifile.replace(".csv","tab")
        tabname=tabname.replace("/","")
        tabname=tabname.replace("_","")
        return(tabname)

#    def csvtex(self,ofile,cap):
#        output=self.create_tex(cap)
#        if ofile:
#            ofile=re.sub('.csv', '.tex', self.ifile) # csv to tex 
#            with open(ofile,'w') as f: f.write(output)
#            print(f"csv2tex: {self.ifile} -> {ofile}")
#        return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert csv file to latex *tex format (normally called from rpt2tex.py)',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--cap", type=str, default="",
            help="Add caption. This also makes table visible i.e not a tab(default: %(default)s)")

    parser.add_argument( "--ifile", type=str, default="data/TK_GB_rpt.csv",
            help="ifile containing containing initial csv file (default: %(default)s)")

#    parser.add_argument("--ofile", action="store_true",
#            help="Send output to file (called ifile.tex)")

    argv=parser.parse_args()

#    df = pd.read_csv(self.ifile,comment= '#')
#    print("Get ifile")
    tex=csv2tex(argv.ifile)
#    output=tex.csvtex(argv.ofile,argv.cap)
    output=tex.create_tex(argv.cap)
#    print (output)
