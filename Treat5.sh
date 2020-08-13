# Sun 10 July 2020 Generate results
#set -x
# Create 3 models
./Treat5.py --model "GB_vif" --cref "RF_vif"
./Treat5.py --model "GB_vif" --cref "LR"
./Treat5.py --model "GB_vif" --cref "DT"
# Manually create file data/GB_vif_cap2_RF_vif_LR_DT_cref.csv
