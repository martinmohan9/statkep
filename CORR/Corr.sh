#!/bin/sh
#   author:martinmhan@yahoo.com date:  22/04/2020
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

#set -x

if [ $# -eq 0 ]
then
    ifile="data/TK_vif.csv"
    datadir="dataCorr/"
    oname="After"
    echo "PostVif $ifile $datadir oname=$oname"
else
    ifile="data/TK_novif.csv"
    datadir="dataCorr_novif/"
    oname="Before"
    echo "_novif using $ifile $datadir oname=$oname"
fi

#echo test$oname
#exit

./Corr.R --rmin 0.00 --rmax 0.05 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.10 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.15 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.20 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.25 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.30 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.35 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.40 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.45 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.50 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.55 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.60 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.65 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.70 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.75 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.80 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.85 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.90 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.95 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 1.0 --corr --hmap --ifile $ifile --odir $datadir

./Corr.R --rmin 0.005 --rmax 1.0 --corr --hmap --ifile $ifile --odir $datadir
# Before --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.05 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.00 --rmax 0.10 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.05 --rmax 0.10 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.10 --rmax 0.15 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.15 --rmax 0.20 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.20 --rmax 0.25 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.25 --rmax 0.30 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.30 --rmax 0.35 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.35 --rmax 0.40 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.40 --rmax 0.45 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.45 --rmax 0.50 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.50 --rmax 0.55 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.55 --rmax 0.60 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.60 --rmax 0.65 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.65 --rmax 0.70 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.70 --rmax 0.75 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.75 --rmax 0.80 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.80 --rmax 0.85 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.85 --rmax 0.90 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.90 --rmax 0.95 --corr --hmap --ifile $ifile --odir $datadir
./Corr.R --rmin 0.95 --rmax 1.0 --corr --hmap --ifile $ifile --odir $datadir
## Do not start at 0

./Corr.R --rmin 0.005 --rmax 1.0 --corr --hmap --ifile $ifile --odir $datadir
cp $datadir/0.005_1TCE2hmap.pdf ../config/figures/hmap$oname.pdf
./Corr.py --odir $datadir
cp $datadir/Corr.py.pdf ../Report/figures/Corr$oname.png
