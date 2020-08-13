#!/bin/sh
#./CorrPreVIF.sh
#./CorrPostVIF.sh 

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
    echo "Previf using $ifile $datadir oname=$oname"
fi

set -x
./Corr.R --rmin 0.005 --rmax 1.0 --corr --hmap --ifile $ifile --odir $datadir
cp $datadir/0.005_1TCE2hmap.pdf ../config/figures/hmap$oname.pdf

if [ $oname = "After" ]
then
#    echo "After == green"
    ./Corr.py --odir $datadir --color "darkorange"
else
    ./Corr.py --odir $datadir --color "red"
fi


cp $datadir/Corr.py.pdf ../Report/figures/Corrhist$oname.pdf
set +x
