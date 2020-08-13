#usage: Treat2.py [-h] [--ifile IFILE] [--bin | --cap | --pca | --vif]
#
#Read files data/TK.csv and data/TCE1.csv created by Treat1.py. Create new file
#depending on options e.g --b bTK.csv, bTCE.csv --out create
#TK_out.csv,TCE1_out.csv
#
#optional arguments:
#  -h, --help     show this help message and exit
#  --ifile IFILE  input file (default: data/TK.csv)
#  --bin          koi_disposition (DV): Create CONFIRMED vs REST file
#                 binary(bin) add TK=>bTK (i.e merge CANDIDATE with FALSE
#                 POSITIVE) (default: False)
#  --cap          Cap Outliers 5qtile and 95qtile. NB TCE1 is also be modified
#                 to TCE1_cap: (default: False)
#  --pca          Product Component Analysis (pc) (default: False)
#  --vif          Remove multicorrelatd ivs and save filename __vif (default:
#                 False)
# Order is important
# Create binary
./Treat2.py --ifile "data/TK.csv" --bin

# Create vif
./Treat2.py --ifile "data/TK.csv" --vif
./Treat2.py --ifile "data/bTK.csv" --vif
./Treat2.py --ifile "data/TCE1.csv" --vif
./Treat2.py --ifile "data/bTCE1.csv" --vif

# Create cap (cap1 selected, cap2 all)
./Treat2.py --ifile "data/TK_vif.csv" --cap1
./Treat2.py --ifile "data/bTK_vif.csv" --cap1
./Treat2.py --ifile "data/TCE1_vif.csv" --cap1
./Treat2.py --ifile "data/bTCE1_vif.csv" --cap1

./Treat2.py --ifile "data/TK_vif.csv" --cap2
./Treat2.py --ifile "data/bTK_vif.csv" --cap2
./Treat2.py --ifile "data/TCE1_vif.csv" --cap2
./Treat2.py --ifile "data/bTCE1_vif.csv" --cap2

# Create pca
./Treat2.py --ifile "data/TK_vif_cap2.csv" --pca
./Treat2.py --ifile "data/bTK_vif_cap2.csv" --pca
./Treat2.py --ifile "data/TCE1_vif_cap2.csv" --pca
./Treat2.py --ifile "data/bTCE1_vif_cap2.csv" --pca

# Create normalized pca not needed
#./Treat2.py --ifile "data/TK_vif_cap2.csv" --npca
#./Treat2.py --ifile "data/bTK_vif_cap2.csv" --npca
#./Treat2.py --ifile "data/TCE1_vif_cap2.csv" --npca
#./Treat2.py --ifile "data/bTCE1_vif_cap2.csv" --npca
