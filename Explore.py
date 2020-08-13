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
import pandas as pd
import argparse,sys
#https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module

# This is just for test
def mult(factor_1, factor_2):
    """ Simple function to be tested """
    return factor_1 * factor_2

def rows_cols(df,name):
    rows,cols=df.shape[0],df.shape[1]
    print(name,rows,cols)

#args = parse_args(sys.argv[1:])
parser = argparse.ArgumentParser(description='Explore the contents of a kepler CSV file',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "csv",
    type=str,
    default="data/tce.csv",
    help="Explore csv files at different levels of verbosity. The output can be piped into other commands such as grep")

parser.add_argument("-v","--verbose", action="count",default=0,
            help="increase verbosity using -v,-vv,-vvv")

#group = parser.add_mutually_exclusive_group()
#group.add_argument("-c","--correlated", action="store_true", help="Output correlated values")

args=parser.parse_args()

#print("Checking file %s verbose=%s" %(args.csv,args.verbose))
tce = pd.read_csv(args.csv,comment= '#')
#if (args.verbose > 2):
# print all cols

if (args.verbose > 2):
    print("info :%s" %tce.info(verbose=True))

if (args.verbose > 1):
    print("%s" %(tce.head()))

if (args.verbose > 0):
    print("info :%s" %tce.info(verbose=False))

if (args.verbose ==0 ):
    print("rows %d,cols %d" %(tce.shape[0],tce.shape[1]))
