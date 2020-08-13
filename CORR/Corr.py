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
import matplotlib.pyplot as plt
import argparse,sys

parser = argparse.ArgumentParser(description='Creates a Histogram by counting columns in csv files. You must first run ./Corr.sh which produces files based on correlation limits')

parser.add_argument( "--odir", type=str, default="dataCorr",
    help="Directory with files (default: %(default)s)")

parser.add_argument( "--color", type=str, default="red",
    help="Color or ticks and label (default: %(default)s)")

args=parser.parse_args()

# Read in x and y(number of columns)
# -4 koi_disposition,kepid and  kepoi_name were not measured
# and pairs are matched -1
#CorrDir="./dataCorr/"
CorrDir="./"+args.odir+"/"
#"./dataCorr/"
histdict = {}
histdict["0.00-0.05"]=pd.read_csv(CorrDir+"0_0.05TCE2.csv").shape[1]-4
histdict["0.05-0.10"]=pd.read_csv(CorrDir+"0.05_0.1TCE2.csv").shape[1]-4
histdict["0.10-0.15"]=pd.read_csv(CorrDir+"0.1_0.15TCE2.csv").shape[1]-4
histdict["0.15-0.20"]=pd.read_csv(CorrDir+"0.15_0.2TCE2.csv").shape[1]-4
histdict["0.20-0.25"]=pd.read_csv(CorrDir+"0.2_0.25TCE2.csv").shape[1]-4
histdict["0.25-0.30"]=pd.read_csv(CorrDir+"0.25_0.3TCE2.csv").shape[1]-4
histdict["0.30-0.35"]=pd.read_csv(CorrDir+"0.3_0.35TCE2.csv").shape[1]-4
histdict["0.35-0.40"]=pd.read_csv(CorrDir+"0.35_0.4TCE2.csv").shape[1]-4
histdict["0.40-0.45"]=pd.read_csv(CorrDir+"0.4_0.45TCE2.csv").shape[1]-4
histdict["0.45-0.50"]=pd.read_csv(CorrDir+"0.45_0.5TCE2.csv").shape[1]-4
histdict["0.50-0.55"]=pd.read_csv(CorrDir+"0.5_0.55TCE2.csv").shape[1]-4
histdict["0.55-0.60"]=pd.read_csv(CorrDir+"0.55_0.6TCE2.csv").shape[1]-4
histdict["0.60-0.65"]=pd.read_csv(CorrDir+"0.6_0.65TCE2.csv").shape[1]-4
histdict["0.65-0.70"]=pd.read_csv(CorrDir+"0.65_0.7TCE2.csv").shape[1]-4
histdict["0.70-0.75"]=pd.read_csv(CorrDir+"0.7_0.75TCE2.csv").shape[1]-4
histdict["0.75-0.80"]=pd.read_csv(CorrDir+"0.75_0.8TCE2.csv").shape[1]-4
histdict["0.80-0.85"]=pd.read_csv(CorrDir+"0.8_0.85TCE2.csv").shape[1]-4
histdict["0.85-0.90"]=pd.read_csv(CorrDir+"0.85_0.9TCE2.csv").shape[1]-4
histdict["0.90-0.95"]=pd.read_csv(CorrDir+"0.9_0.95TCE2.csv").shape[1]-4

import os.path
if os.stat(CorrDir+"0.95_1TCE2.csv").st_size==0:
    histdict["0.95-1.00"]=0
else:
    histdict["0.95-1.00"]=pd.read_csv(CorrDir+"0.95_1TCE2.csv").shape[1]-4


#print (f"histdict= {histdict} sum.values= {sum(histdict.values())}")

x=list(histdict.keys())
y=list(histdict.values())
x_labels=list(histdict.keys())

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

fig, (ax) = plt.subplots(1)                                             
ax.bar(x,y,align='center') # A bar chart
ax.set_xlabel('Pearson’s Correlation Coefficient (R) - Independent Variables')
ylab="Frequency (Total = "+str(sum(histdict.values()))+")"
#ax.set_ylabel(ylab,color="green",weight="ultrabold",size="x-large",style="italic")
ax.xaxis.set_ticklabels(x)
ax.set_ylabel(ylab,color=args.color,size="x-large",style="italic")
ax.get_xticklabels()[18].set_color(args.color)
ax.get_xticklabels()[19].set_color(args.color)
plt.xticks(rotation=70)
ax.get_xticklabels()
fname=CorrDir+sys.argv[0]+".pdf"
plt.savefig(fname)  
print("Plot saved as %s" %fname)
plt.show()
