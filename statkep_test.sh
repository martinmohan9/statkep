#!/bin/sh
###!/bin/bash
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

#set -x
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

colorTest(){
    echo "${RED}red text ${GREEN}green text${NC} xxx no color"
    echo "${red}red text ${green}green text${reset} xxx reset"
}
#colorTest "one" "two"

equalF() # Passed $a and $b
{
DIFF=$(diff $1 $2)
diff=$?

if [ $diff -eq 0 ]
then
    echo "${green}pass:${reset} $1 == $2"
elif [ $diff -eq 1 ] # different
then
    echo "${red}fail:${reset} $1 != $2"
#elif [ $diff -eq 2 ] # Missing
#else
#    echo "fail: Missing file"
fi
}

createdF()
{
FILE=$1
if test -f "$FILE"; then
    echo "${green}pass:${reset} $FILE ${green}created${reset}"
else
    echo "${red}fail:${reset} $FILE ${red}not created${reset}"
fi
}

existF()
{
FILE=$1
if test -f "$FILE"; then
    echo "${green}pass:${reset} $FILE ${green}exists${reset}"
else
    echo "${red}fail:${reset} $FILE ${red}missing${reset}"
fi
}

if [ $# -eq 0 ] || [ "${1#*.}" = "-h" ]; then
    echo "$0 T1,T2,T3,T4,T5 or myfit to select test"
fi

# Initial files
#if [[ -n "$1" ]] && [[ "${1#*.}" == "T4" ]]; then
equalF "data/TCE.csv" " data/TCE.csv.T0"
equalF "data/KOI.csv" "data/KOI.csv.T0"

if [ $# -eq 0 ] || [ "${1#*.}" = "T1" ]; then
echo "run ./Treat1.py test"
rm data/TK.csv data/TCE1.csv
./Treat1.py > /dev/null
equalF "data/TK.csv" "data/TK.csv.T1"
equalF "data/TCE1.csv" "data/TCE1.csv.T1"
fi

if [ $# -eq 0 ] || [ "${1#*.}" = "T2" ]; then
echo "run ./Treat2.sh test"

#rm data/bTCE1_vif_cap2_pca.csv data/TCE1_vif_cap2_pca.csv  data/bTK_vif_cap2_pca.csv data/TK_vif_cap2_pca.csv data/bTCE1_vif_cap2.csv data/TCE1_vif_cap2.csv  data/bTK_vif_cap2.csv data/TK_vif_cap2.csv data/bTCE1_vif_cap1.csv data/TCE1_vif_cap1.csv  data/bTK_vif_cap1.csv data/TK_vif_cap1.csv data/bTCE1_vif.csv data/TCE1_vif.csv  data/bTK_vif.csv data/TK_vif.csv data/bTCE1.csv data/bTK.csv
rm data/bTCE1_vif_cap2_pca.csv data/TCE1_vif_cap2_pca.csv  data/bTK_vif_cap2_pca.csv data/TK_vif_cap2_pca.csv data/bTCE1_vif_cap2.csv data/TCE1_vif_cap2.csv  data/bTK_vif_cap2.csv data/TK_vif_cap2.csv data/bTCE1_vif_cap1.csv data/TCE1_vif_cap1.csv  data/bTK_vif_cap1.csv data/TK_vif_cap1.csv data/bTCE1_vif.csv data/TCE1_vif.csv  data/bTK_vif.csv data/TK_vif.csv data/bTCE1.csv data/bTK.csv
./Treat2.sh > /dev/null
#equalF "data/bTCE1_vif_cap2_pca.csv" "data/bTCE1_vif_cap2_pca.csv.T2"
equalF "data/TCE1_vif_cap2_pca.csv" "data/TCE1_vif_cap2_pca.csv.T2"
#equalF "data/bTK_vif_cap2_pca.csv" "data/bTK_vif_cap2_pca.csv.T2"
equalF "data/TK_vif_cap2_pca.csv" "data/TK_vif_cap2_pca.csv.T2"
#equalF "data/bTCE1_vif_cap2.csv" "data/bTCE1_vif_cap2.csv.T2"
equalF "data/TCE1_vif_cap2.csv" "data/TCE1_vif_cap2.csv.T2"
#equalF "data/bTK_vif_cap2.csv" "data/bTK_vif_cap2.csv.T2"
equalF "data/TK_vif_cap2.csv" "data/TK_vif_cap2.csv.T2"
#equalF "data/bTCE1_vif_cap1.csv" "data/bTCE1_vif_cap1.csv.T2"
equalF "data/TCE1_vif_cap1.csv" "data/TCE1_vif_cap1.csv.T2"
#equalF "data/bTK_vif_cap1.csv" "data/bTK_vif_cap1.csv.T2"
equalF "data/TK_vif_cap1.csv" "data/TK_vif_cap1.csv.T2"
#equalF "data/bTCE1_vif.csv" "data/bTCE1_vif.csv.T2"
equalF "data/TCE1_vif.csv" "data/TCE1_vif.csv.T2"
#equalF "data/bTK_vif.csv" "data/bTK_vif.csv.T2"
equalF "data/TK_vif.csv" "data/TK_vif.csv"
#equalF "data/bTCE1.csv" "data/bTCE1.csv.T2"
#equalF "data/bTK.csv" "data/bTK.csv.T2"
fi

if [ $# -eq 0 ] || [ "${1#*.}" = "T3" ]; then
echo "run ./Treat3.py test - min of 3 mins"
rm "data/TK_100g_None_Tpot.py" "data/TK_100g_Tpot_light_Tpot.py" "data/TK_100g_LR_Tpot.py"
./Treat3.py --max_time_mins 1 > /dev/null
./Treat3.py --model Tpot_light --max_time_mins 1 > /dev/null
./Treat3.py --model LR --max_time_mins 1 > /dev/null
createdF "data/TK_100g_None_Tpot.py"
createdF "data/TK_100g_Tpot_light_Tpot.py"
createdF "data/TK_100g_LR_Tpot.py"
fi

if [ $# -eq 0 ] || [ "${1#*.}" = "T4" ]; then
echo "run ./Treat4.py tests"
# Start T4 only GB tested
#existF "data/TKtest_GB.pickle"
#existF "data/bTKtest_bGB.pickle"
existF "data/GBtest.pickle"
#existF "data/bGBtest.pickle"

#find data -name bTKtest*_bGB* -type f -writable -delete
find data -name *GBTest* -type f -writable -delete
#./Treat4.py --ifile data/TKtest.csv --model GBtest > /dev/null
#./Treat4.py --ifile data/bTKtest.csv --model bGBtest > /dev/null
./Treat4.py --model GBtest > /dev/null
#./Treat4.py --model bGBtest > /dev/null

#equalF "data/bGBtest_roc.tex" "data/bGBtest_roc.tex.T4"
#equalF "data/bGBtest_metric.csv" "data/bGBtest_metric.csv.T4"
equalF "data/GBtest_roc.tex" "data/GBtest_roc.tex.T4"
equalF "data/GBtest_metric.csv" "data/GBtest_metric.csv.T4"

#createdF "data/bGBtest_overfit_cm.pdf"
#createdF "data/bGBtest_overfit_roc.pdf"
#createdF "data/bGBtest_cm.pdf"
#createdF "data/bGBtest_roc.pdf"
createdF "data/GBtest_overfit_cm.pdf"
createdF "data/GBtest_overfit_roc.pdf"
createdF "data/GBtest_cm.pdf"
createdF "data/GBtest_roc.pdf"
createdF "data/GBtest.pickle"
createdF "data/bGBtest.pickle"
fi

if [ $# -eq 0 ] || [ "${1#*.}" = "T5" ]; then
echo "run ./Treat5.py tests"
rm "data/LR_confirm.csv"
find data -name *LR_pred_* -type f -writable -delete
./Treat5.py > /dev/null
equalF "data/LR_pred_confirm.tex" "data/LR_pred_confirm.tex.T5"
equalF "data/LR_confirm.csv" "data/LR_confirm.csv.T5"
#equalF "data/LR_pred.csv" "data/LR_pred.csv.T5"
equalF "data/GB_vif_RF_vif_LR_DT.tex" "data/GB_vif_RF_vif_LR_DT.tex.T5"
equalF "data/GB_vif_RF_vif_LR_DT.csv" "data/GB_vif_RF_vif_LR_DT.csv.T5"
createdF "data/LR_pred_confirm.pdf"

fi

if [ $# -eq 0 ] || [ "${1#*.}" = "myfit" ]; then
echo "run myfit test"
rm "data/GB_res.csv"
./myfit.py
equalF "data/GB_res.csv" "data/GB_res.csv.T4"
fi

if [ $# -eq 0 ] || [ "${1#*.}" = "csv2tex" ]; then
echo "run csv2tex test"
#rm "data/GB_res.csv"
#./myfit.py
#equalF "data/GB_res.csv" "data/GB_res.csv.T4"
fi

