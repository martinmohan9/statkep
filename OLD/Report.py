# Sun 10 July 2020 Generate results
#set -x
#"LR": "sklearn.linear_model.LogisticRegression,0.840,Found using TPOT light,0.804",
#"bLR_vif": "sklearn.linear_model.LogisticRegression,0.894,Found using TPOT light,0.834",
#"bLR_vif_cap1": "sklearn.tree.DecisionTreeClassifier,0.897,Found using TPOT light,",
#"bLR_vif_cap2": "sklearn.linear_model.LogisticRegression,0.903,Found using TPOT light,0.831",

#"RF": "sklearn.ensemble.RandomForestClassifier,0.858,TPOT coerced to use Random Forest,0.812",
#"RF_vif": "sklearn.ensemble.RandomForestClassifier,?,,",
#"bRF": "sklearn.ensemble.RandomForestClassifier,0.944,Coerced to use Random Forest,0.844",
#"bRF_vif": "sklearn.ensemble.RandomForestClassifier,0.915,,0.847",
#"bRF_vif_cap2": "sklearn.ensemble.RandomForestClassifier,?,,?",

#Choose RF and LR

\section{Evaluation}
Prediction using binary class provided a slightly higher accuracy but the distinction between CANDIDATES and False Positives was lost so multi-class solutions were preferred. Planets unrecorded by NASA were recovered using different models although further checks are needed see discussion.
\subsection{Logistic Regression}
Logistic Regression model had a good precision in getting recovered planets as shown in \figurename~\ref{fig:data/LR_roc} 
./Treat4.py --model "LR"
\input{data/LR_roc}
\subsection{Random Forest}
./Treat4.py --model "RF"
\input{data/RF_roc}
./Treat5.py --model "LR" --cref "RF"
./csv2tex.py --ifile data/RF_cref.csv --ofile
\input{data/RF_cref}

\subsection{Random Forest}
\input{data/RF_roc}
\subsection{Random Forest Recovery}
\input{data/RF_pred_CONFIRMED.tex}
\subsection{Logistic Regression}
\input{data/LR_ROC}
\subsection{Logistic Regression Recovery}
\input{data/LR_pred_CONFIRMED.tex}
\subsection{Cross Reference Results}
\input{data/RF_LR_cref}

