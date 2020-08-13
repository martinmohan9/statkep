# Sun 10 July 2020 Generate results
#set -x
./Treat4.py --ifile data/TK.csv --model "DT" --fit
./Treat4.py --ifile data/TK.csv --model "GB" --fit
./Treat4.py --ifile data/TK.csv --model "LR" --fit
./Treat4.py --ifile data/TK.csv --model "RF" --fit
 --fit
./Treat4.py --ifile data/bTK.csv --model "bDT" --fit
./Treat4.py --ifile data/bTK.csv --model "bGB" --fit
./Treat4.py --ifile data/bTK.csv --model "bLR" --fit
./Treat4.py --ifile data/bTK.csv --model "bRF" --fit
 --fit
./Treat4.py --ifile data/TK_vif.csv --model "DT_vif" --fit
./Treat4.py --ifile data/TK_vif.csv --model "GB_vif" --fit
./Treat4.py --ifile data/TK_vif.csv --model "LR_vif" --fit
./Treat4.py --ifile data/TK_vif.csv --model "RF_vif" --fit
 --fit
./Treat4.py --ifile data/bTK_vif.csv --model "bDT_vif" --fit
./Treat4.py --ifile data/bTK_vif.csv --model "bGB_vif" --fit
./Treat4.py --ifile data/bTK_vif.csv --model "bLR_vif" --fit
./Treat4.py --ifile data/bTK_vif.csv --model "bRF_vif" --fit
 --fit
./Treat4.py --ifile data/TK_vif_cap2.csv --model "DT_vif_cap2" --fit
./Treat4.py --ifile data/TK_vif_cap2.csv --model "GB_vif_cap2" --fit
./Treat4.py --ifile data/TK_vif_cap2.csv --model "LR_vif_cap2" --fit
./Treat4.py --ifile data/TK_vif_cap2.csv --model "RF_vif_cap2" --fit
 --fit
./Treat4.py --ifile data/bTK_vif_cap2.csv --model "bDT_vif_cap2" --fit
./Treat4.py --ifile data/bTK_vif_cap2.csv --model "bGB_vif_cap2" --fit
./Treat4.py --ifile data/bTK_vif_cap2.csv --model "bLR_vif_cap2" --fit
./Treat4.py --ifile data/bTK_vif_cap2.csv --model "bRF_vif_cap2" --fit
