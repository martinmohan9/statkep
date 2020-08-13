#!/usr/bin/env python
# coding: utf-8
#   author:martinmhan@yahoo.com date:  04/07/2020
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

import argparse
import csv2tex

import argparse
import csv2tex

class rpt2tex2():
    def __init__(self):
        pass

    def roctex2(self,froc,fcm,fcsv,caption,cref,crefonly):
        csvfile=csv2tex.csv2tex(fcsv)
        rpttab=csvfile.generatetab()

        if crefonly:
            label=cref.replace(".pdf","")
            ftex=cref.replace(".pdf",".tex")

            output="\n\\begin{figure}[H]\n\
                \\centering\n\
	        \\includegraphics[width=1\\textwidth,height=.4\\textheight]{%s}\n\
                \\caption{%sPlanets predicted as CONFIRMED}\n\
                \\label{fig:%s}\n\
                \\end{figure}" %(cref,caption,label)
        else:
            label=fcsv.replace(".csv","")
            ftex=fcsv.replace(".csv",".tex")

            output="\n\\begin{figure}[H]\n\
                \\centering\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{1\\textwidth}\n\
                \\csname %s\\endcsname\n\
                \\end{subfigure}\n\
                \\caption{%sConfusion Matrix, ROC Curve and Results}\n\
                \\label{fig:%s}\n\
                \\end{figure}" %(froc,fcm,rpttab,caption,label)

        with open(ftex,'w') as f: f.write(output)
#        print(f"Created file {ftex}")
        return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read rpt files generated by Treat4.py and create latex tex file including  _roc.pdf, _cm.pdf, _rpt.csv (normlly called from Treat4.py)',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--froc", type=str, default="data/TK_GB_roc.pdf",
            help="roc pdf (default: %(default)s)")

    parser.add_argument( "--fcm", type=str, default="data/TK_GB_cm.pdf",
            help="cm pdf (default: %(default)s)")

    parser.add_argument( "--fcsv", type=str, default="data/TK_GB_rpt.csv",
            help="csv file (default: %(default)s)")

    parser.add_argument( "--cref", type=str, default="data/TKtest_GB_cref_CONFIRMED.pdf",
            help="Add cref file - set to '' to ignore (default: %(default)s)")

    parser.add_argument("--crefonly", action="store_true",
        help="Only ouput cref")

    parser.add_argument( "--caption", type=str, default="",
            help="caption (default: %(default)s)")

    argv=parser.parse_args()

    myrpt=rpt2tex2()
    output=myrpt.roctex2(argv.froc,argv.fcm,argv.fcsv,argv.caption,argv.cref,argv.crefonly)
    print(output)
