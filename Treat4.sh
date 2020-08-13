# Sun 10 July 2020 Generate results
set -x
#./Treat4.py --model "XGB" --fit
#./Treat4.py --model "XGB_vif" --fit
#./Treat4.py --model "XGB_vif_cap2" --fit

#./Treat4.py --model "DT" --fit
#./Treat4.py --model "DT_vif" --fit
#./Treat4.py --model "DT_vif_cap2" --fit

#./Treat4.py --model "RF" --fit
#./Treat4.py --model "RF_vif" --fit
#./Treat4.py --model "RF_vif_cap2" --fit

#./Treat4.py --model "GB" --fit
#./Treat4.py --model "GB_vif" --fit
#./Treat4.py --model "GB_vif_cap2" --fit

#./Treat4.py --model "LR" --fit
#./Treat4.py --model "LR_vif" --fit
#./Treat4.py --model "LR_vif_cap2" --fit

./Treat4.py --model "SVC" --fit
./Treat4.py --model "XGB" --fit
./Treat4.py --model "XGB_vif" --fit
./Treat4.py --model "XGB_vif_cap2" --fit
