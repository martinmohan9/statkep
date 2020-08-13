# usage: Treat1.py [-h] [--tcefile TCEFILE] [--koifile KOIFILE] [--TCEiv]
# Merge data/TCE.csv and data/KOI.csv (or add koi_dispostion from KOI.csv) then
# drop, factorize or modify cols. The default output is 'TK.csv' (or 'TKiv.csv'
# ).
# 
# optional arguments:
#   -h, --help         show this help message and exit
#   --tcefile TCEFILE  tce file contains all the IV's (default: data/TCE.csv)
#   --koifile KOIFILE  koi file used to obtain DV (default: data/KOI.csv)
#   --TCEiv            'TCEiv.csv' file with ivs created from TCE.csv. Same
#                      treatment as before drop cols etc... but no merging with
#                      KOI (default: False)
./Treat1.py # Default will create a file TK.csv add options
./Treat1.py --TCEiv # Create TCEiv.csv
# TODO remove options not needed
