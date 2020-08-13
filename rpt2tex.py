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

class rpt2tex():
    def __init__(self,pdffile):

        #        print(f'pdffile is  {pdffile}')
        if not pdffile.endswith(".pdf"):
            print('Need at least one pic ending in ".pdf"')
            sys.exit(0)
        self.label=pdffile.replace(".pdf","")
        self.pdffile=pdffile
#        print(f'Label is  {self.label}')


    def ROCs(self,fpic1,fpic2,fpic3,fpic4,fcsv,caption):
        csvfile=csv2tex.csv2tex(fcsv)
        rpttab=csvfile.generatetab()
#        csvoutput=csvfile.csvtex()
        csvoutput=csvfile.create_tex(caption="")
        label=self.label
        ftex=label+".tex"

        output="\n\\begin{figure}[H]\n\
                \\begin{mdframed}[linecolor=green]\n\
                \\centering\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{1\\textwidth}\n\
                \\csname %s\\endcsname\n\
                \\end{subfigure}\n\
                \\caption{%s}\n\
                \\label{fig:%s}\n\
                \\end{mdframed}\n\
                \\end{figure}" %(fpic1,fpic2,fpic3,fpic4,rpttab,caption,label)
        output=csvoutput+output

        with open(ftex,'w') as f: f.write(output)
        print(f"rpt2tex:ROCs: Created file {ftex} using {self.pdffile}")
        return output

    def p1c1(self,fpic1,fcsv,caption):
        csvfile=csv2tex.csv2tex(fcsv)
        rpttab=csvfile.generatetab()
        csvoutput=csvfile.csvtex()
        label=self.label
        ftex=label+".tex"

        output="\n\\begin{figure}[H]\n\
                \\centering\n\
                \\begin{subfigure}{1\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{1\\textwidth}\n\
                \\csname %s\\endcsname\n\
                \\end{subfigure}\n\
                \\caption{%s}\n\
                \\label{fig:%s}\n\
                \\end{figure}" %(fpic1,rpttab,caption,label)
        output=csvoutputp+output

        with open(ftex,'w') as f: f.write(output)
        print(f"rpt2tex:p1c1: Created file {ftex} using {self.pdffile}")
        return output

    def p3c1(self,fpic1,fpic2,fpic3,fcsv,caption=""):
        """ Use for latex displaying 3 pictures above a table roc,cm,recover and metrics. """
        csvfile=csv2tex.csv2tex(fcsv)
        rpttab=csvfile.generatetab()
        csvoutput=csvfile.csvtex()

#        label=label+"p3c1"
        label=self.label
        ftex=label+".tex"

        output="\n\\begin{figure}[H]\n\
                \\centering\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{1\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{1\\textwidth}\n\
                \\csname %s\\endcsname\n\
                \\end{subfigure}\n\
                \\caption{%s}\n\
                \\label{fig:%s}\n\
                \\end{figure}" %(fpic1,fpic2,fpic3,rpttab,caption,label)
        output=csvoutput+output

        with open(ftex,'w') as f: f.write(output)
        print(f"rpt2tex:p3c1: Created file {ftex} using {self.pdffile}")
        return output

    def p1(self,fpic1,caption=""):
        """ Display a single picture. """
#        label=self.label+"p1"
        label=self.label
        ftex=label+".tex"

        output="\n\\begin{figure}[H]\n\
                \\begin{mdframed}[linecolor=green]\n\
                \\centering\n\
                \\includegraphics[width = 1\\textwidth,height=.4\\textheight]{%s}\n\
                \\caption{%s}\n\
                \\label{fig:%s}\n\
                \\end{mdframed}\n\
                \\end{figure}" %(fpic1,caption,label)

        with open(ftex,'w') as f: f.write(output)
        print(f"rpt2tex:p1: Created file {ftex} using {self.pdffile}")
        return output

    def p2(self,fpic1,fpic2,caption=""):
        """ Display 2 pictures side by side roc,cm. """

#        label=self.label+"p2"
        label=self.label
        ftex=label+".tex"

        output="\n\\begin{figure}[H]\n\
                \\centering\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\begin{subfigure}{.49\\textwidth}\n\
                \\includegraphics[width = 1\\textwidth]{%s}\n\
                \\end{subfigure}\n\
                \\caption{%s}\n\
                \\label{fig:%s}\n\
                \\end{figure}" %(fpic1,fpic2,caption,label)

        with open(ftex,'w') as f: f.write(output)
        print(f"rpt2tex:p2: Created file {ftex} using {self.pdffile}")
        return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read rpt files generated by Treat4.py and create latex tex file including  _roc.pdf, _cm.pdf, _rpt.csv (normlly called from Treat4.py)',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( "--fpic1", type=str, default="data/TK_GB_roc.pdf",
            help="fpic1 eg roc.pdf MUST be supplied for naming (default: %(default)s)")

    parser.add_argument( "--fpic2", type=str, default="data/TK_GB_cm.pdf",
            help="fpic2 eg. cm.pdf (default: %(default)s)")

    parser.add_argument( "--fpic3", type=str, default="data/TK_GB_cref_CONFIRMED.pdf",
            help="fpic3 e.g cref.pdf file (default: %(default)s)")

    parser.add_argument( "--fcsv", type=str, default="data/TK_GB_rpt.csv",
            help="csv report file (default: %(default)s)")

    parser.add_argument( "--caption", type=str, default="",
            help="caption (default: %(default)s)")

    parser.add_argument('--type', choices=['p1', 'p2','p3c1'], default="p1",
            help='Type of content pic 1, pics 3, pics 3 and csv 1 file')

    argv=parser.parse_args()

    myrpt=rpt2tex(argv.fpic1)
    if argv.type=='p1': 
        output=myrpt.p1(argv.fpic1,argv.caption)
    elif argv.type=='p2': 
        output=myrpt.p2(argv.fpic1,argv.fpic2,argv.caption)
    elif argv.type=='p3c1': 
        output=myrpt.p3c1(argv.fpic1,argv.fpic2,argv.fpic3,argv.fcsv,argv.caption)
    else: 
        output=f"Unknown type {argv.type}"
#    print(output)
#    output=myrpt.roctex(argv.pic1,argv.pic2,argv.fcsv,argv.caption,argv.cref,argv.crefonly)
