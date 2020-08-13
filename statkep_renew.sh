# After --fit values will change - so csv and pickle are write protected
rm data/TK.csv.T4 data/TCE1.csv.T4
cp "data/TK.csv" "data/TK.csv.T4"
cp "data/TCE1.csv" "data/TCE1.csv.T4"
chmod u-w data/TK.csv.T4 data/TCE1.csv.T4

rm data/bTCE1.csv.T4 data/TK_vif.csv.T4 data/TCE1_vif.csv.T4 data/bTK_vif.csv.T4 data/bTCE1_vif.csv.T4
cp "data/bTK.csv" "data/bTK.csv.T4"
cp "data/TCE1.csv" "data/TCE1.csv.T4"
cp "data/TCE1.csv" "data/bTCE1.csv.T4" # TCE1.csv = bTCE1.csv
cp "data/TK_vif.csv" "data/TK_vif.csv.T4"
cp "data/TCE1_vif.csv" "data/TCE1_vif.csv.T4"
cp "data/bTK_vif.csv" "data/bTK_vif.csv.T4"
cp "data/bTCE1_vif.csv" "data/bTCE1_vif.csv.T4"
chmod u-w data/bTCE1.csv.T4 data/TK_vif.csv.T4 data/TCE1_vif.csv.T4 data/bTK_vif.csv.T4 data/bTCE1_vif.csv.T4
exit

echo "To force renew: rm -f data/TKtest_GB*T4"
cp "data/TKtest_GB_overfit_roc.tex" "data/TKtest_GB_overfit_roc.tex.T4"
cp "data/TKtest_GB_overfit_cref.csv" "data/TKtest_GB_overfit_cref.csv.T4"
cp "data/TKtest_GB_overfit_rpt.csv" "data/TKtest_GB_overfit_rpt.csv.T4"
chmod u-w data/TKtest_GB_overfit*T4

cp "data/TKtest_GB.pickle" "data/TKtest_GB.pickle.T4"
cp "data/bTKtest_bGB.pickle" "data/bTKtest_bGB.pickle.T4"


cp "data/bTCE1_vif_cap.csv" "data/bTCE1_vif_cap.csv.T4"
cp "data/bTCE1_vif.csv" "data/bTCE1_vif.csv.T4"
cp "data/TCE1_vif_cap.csv" "data/TCE1_vif_cap.csv.T4"
cp "data/TCE1_vif.csv" "data/TCE1_vif.csv.T4"
chmod u-w "data/bTCE1_vif_cap.csv.T4" "data/bTCE1_vif.csv.T4" "data/TCE1_vif_cap.csv.T4" "data/TCE1_vif.csv.T4"

#cp data/bTKtest_bGB_roc.tex data/bTKtest_bGB_roc.tex.T4
#cp data/bTKtest_bGB_metric.csv data/bTKtest_bGB_metric.csv.T4
#cp data/TKtest_GB_roc.tex data/TKtest_GB_roc.tex.T4
#cp data/TKtest_GB_metric.csv data/TKtest_GB_metric.csv.T4
#chmod u-w data/bTKtest_bGB_roc.tex.T4 data/bTKtest_bGB_metric.csv.T4 data/TKtest_GB_roc.tex.T4 data/TKtest_GB_metric.csv.T4

cp "data/bGBtest_roc.tex" "data/bGBtest_roc.tex.T4"
cp "data/bGBtest_metric.csv" "data/bGBtest_metric.csv.T4"
cp "data/GBtest_roc.tex" "data/GBtest_roc.tex.T4"
cp "data/GBtest_metric.csv" "data/GBtest_metric.csv.T4"

chmod u-w data/bGBtest_roc.tex.T4 data/bGBtest_metric.csv.T4 data/GBtest_roc.tex.T4 data/GBtest_metric.csv.T4

cp "data/bRF_vif_pred_CONFIRMED.tex" "data/bRF_vif_pred_CONFIRMED.tex.T4"
cp "data/bRF_vif_cref.csv" "data/bRF_vif_cref.csv.T4"
cp "data/bRF_vif_confirm.csv" "data/bRF_vif_confirm.csv.T4"
cp "data/bRF_vif_pred.csv" "data/bRF_vif_pred.csv.T4"
chmod u-w data/bRF_vif_pred_CONFIRMED.tex.T4 data/bRF_vif_cref.csv.T4 data/bRF_vif_confirm.csv.T4 data/bRF_vif_pred.csv.T4

cp "data/bTCE1_vif_cap2_pca.csv" "data/bTCE1_vif_cap2_pca.csv.T2"
cp "data/TCE1_vif_cap2_pca.csv" "data/TCE1_vif_cap2_pca.csv.T2"
cp "data/bTK_vif_cap2_pca.csv" "data/bTK_vif_cap2_pca.csv.T2"
cp "data/TK_vif_cap2_pca.csv" "data/TK_vif_cap2_pca.csv.T2"
cp "data/bTCE1_vif_cap2.csv" "data/bTCE1_vif_cap2.csv.T2"
cp "data/TCE1_vif_cap2.csv" "data/TCE1_vif_cap2.csv.T2"
cp "data/bTK_vif_cap2.csv" "data/bTK_vif_cap2.csv.T2"
cp "data/TK_vif_cap2.csv" "data/TK_vif_cap2.csv.T2"
cp "data/bTCE1_vif_cap1.csv" "data/bTCE1_vif_cap1.csv.T2"
cp "data/TCE1_vif_cap1.csv" "data/TCE1_vif_cap1.csv.T2"
cp "data/bTK_vif_cap1.csv" "data/bTK_vif_cap1.csv.T2"
cp "data/TK_vif_cap1.csv" "data/TK_vif_cap1.csv.T2"
cp "data/bTCE1_vif.csv" "data/bTCE1_vif.csv.T2"
cp "data/TCE1_vif.csv" "data/TCE1_vif.csv.T2"
cp "data/bTK_vif.csv" "data/bTK_vif.csv.T2"
cp "data/TK_vif.csv" "data/TK_vif.csv"
cp "data/bTCE1.csv" "data/bTCE1.csv.T2"
cp "data/bTK.csv" "data/bTK.csv.T2"
chmod u-w data/bTCE1_vif_cap2_pca.csv.T2 data/TCE1_vif_cap2_pca.csv.T2  data/bTK_vif_cap2_pca.csv.T2 data/TK_vif_cap2_pca.csv.T2 data/bTCE1_vif_cap2.csv.T2 data/TCE1_vif_cap2.csv.T2  data/bTK_vif_cap2.csv.T2 data/TK_vif_cap2.csv.T2 data/bTCE1_vif_cap1.csv.T2 data/TCE1_vif_cap1.csv.T2  data/bTK_vif_cap1.csv.T2 data/TK_vif_cap1.csv.T2 data/bTCE1_vif.csv.T2 data/TCE1_vif.csv.T2  data/bTK_vif.csv.T2 data/TK_vif.csv.T2 data/bTCE1.csv.T2  data/bTK.csv

cp data/TCE.csv data/TCE.csv.T0
cp data/KOI.csv data/KOI.csv.T0
cp data/TK.csv data/TK.csv.T1
cp data/TCE1.csv data/TCE1.csv.T1
chmod u-w data/TCE.csv.T0 data/KOI.csv.T0 data/TK.csv.T1 data/TCE1.csv.T1

cp data/bRF_vif_pred_CONFIRMED.tex data/bRF_vif_pred_CONFIRMED.tex.T5
cp data/bRF_vif_cref.csv data/bRF_vif_cref.csv.T5
cp data/bRF_vif_confirm.csv data/bRF_vif_confirm.csv.T5
cp data/bRF_vif_pred.csv data/bRF_vif_pred.csv.T5

chmod u-w data/bRF_vif_pred_CONFIRMED.tex.T5 data/bRF_vif_cref.csv.T5 data/bRF_vif_confirm.csv.T5 data/bRF_vif_pred.csv.T5


cp "data/GBtest_LR_cref.tex" "data/GBtest_LR_cref.tex.T5"
cp "data/GBtest_LR_cref.csv" "data/GBtest_LR_cref.csv.T5"
cp "data/GBtest_pred_confirm.tex" "data/GBtest_pred_confirm.tex.T5"
cp "data/GBtest_confirm.csv" "data/GBtest_confirm.csv.T5"
cp "data/GBtest_pred.csv" "data/GBtest_pred.csv.T5"

chmod u-w "data/GBtest_LR_cref.tex.T5" "data/GBtest_LR_cref.csv.T5" "data/GBtest_pred_confirm.tex.T5" "data/GBtest_confirm.csv.T5" "data/GBtest_pred.csv.T5"

cp "data/LR_pred_confirm.tex" "data/LR_pred_confirm.tex.T5"
cp "data/LR_confirm.csv" "data/LR_confirm.csv.T5"
cp "data/LR_pred.csv" "data/LR_pred.csv.T5"
cp "data/GB_vif_RF_vif_LR_DT.tex" "data/GB_vif_RF_vif_LR_DT.tex.T5"         


chmod u-w "data/LR_pred_confirm.tex.T5" "data/LR_confirm.csv.T5" "data/LR_pred.csv.T5"
