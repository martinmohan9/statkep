#!/usr/bin/env Rscript
oldw <- getOption("warn")
options(warn = -1)

library(argparse)

parser <- ArgumentParser(description="Calculate naive Bayes AUC, Accuracy etc.. DV=koi_disposition")
parser$add_argument("-v", "--verbose", action="store_true", default=FALSE,
                    help="verbose help [default %(default)s]")
#parser$add_argument("-r", "--retrain", action="store_true", default=TRUE,
#                    help="retrain models [default %(default)s]")
parser$add_argument("-i","--ifile", default="data/TCE1.csv",
                    help="data to be tested - several results files are created [default %(default)s]")
argv <- parser$parse_args()

#suppressPackageStartupMessages(library("caret")) - use suppression later
modeltype="rf"
library(datasets)
library(tidyverse)
library(caret)
library(pROC)

set.seed(18191339)

# Get prediction structure predicted number and probability
# kepid and plnt_nr
#getpred <- function(model,test) {
#    labels=test$koi_disposition
#    pred <- predict(model, test, type = "raw")
#    pred_prob <- predict(model, test, type = "prob")
#
#    results <- data.frame(y_true = labels,
#                          y_pred = pred,
#                          prob_fp = round(pred_prob[ , 2],2),
#                          pCANDIDATE = round(pred_prob[ , 1],2))
#    return(results)
#}

# Sort file by Accuracy
sortA <- function(Fname) {
    # Sort by Accuracy and remove duplicates
    df<-read.csv(Fname,comment='#')
    df<-arrange(df,desc(Accuracy)) # sort by Accuracy
    df[!duplicated(df), ] # remove duplicates
    df[!duplicated(df$Accuracy), ] # remove dup accuracy?
    write.table(format(df, digits=3),Fname, sep = ",",row.names=FALSE, col.names=TRUE, append = FALSE)
    return(Fname)
}

# Create Fpred based on confusion matrix or add line of results
resultTable <- function(mypred,Fres) {
#    results<-caret::confusionMatrix(mypred$y_true,mypred$y_pred)
cmatrix <- caret::confusionMatrix(mypred$y_pred, mypred$y_true,positive='CONFIRMED')

#    cmatrix<-confusionMatrix(mypred$y_true,mypred$y_pred)
    overall<-round(as.matrix(cmatrix, what = "overall"),2)
    classes<-round(as.matrix(cmatrix, what = "classes"),2)
    # AUC
    myroc <- roc(mypred$y_true,mypred$pCANDIDATE)
#    Auc=auc(myroc)
    end_time <- Sys.time()
    model_time<-as.numeric(round(difftime(end_time, start_time,units="secs"),3))
    df<-data.frame(ifile=c(Fname),
                   Accuracy=c(overall["Accuracy",1]),
#                   Accuracy=c(round(overall["Accuracy",1]),
                   Auc=auc(myroc),
                   Kappa=c(overall["Kappa",1]),
                   F1=c(classes["F1","CONFIRMED"]),
                   mtime_sec=c(model_time)
                   #Sensitivity =c(classes["Sensitivity",1]),
    )
    
    if(file.exists(Fres)){
        write.table(format(df, digits=3),Fres, sep = ",",row.names=FALSE, col.names = FALSE, append = T)
    } else{
        write.csv(df, file = Fres, row.names=FALSE)
    }
    # Sort by Accuracy and remove duplicates
    #    df<-read.csv(Fres)
    #    df<-arrange(df,desc(Accuracy)) # sort by Accuracy
    #    df[!duplicated(df), ] # remove duplicates
    #    df[!duplicated(df$Accuracy), ] # remove dup accuracy?
    #    write.table(format(df, digits=3),Fres, sep = ",",row.names=FALSE, col.names=TRUE, append = FALSE)
    return(df)
}

# removeCols - remove cols
removeCols <- function(df) {
    #make.names otherwise caret::model fails
    #df$koi_disposition <- factor(make.names(df$koi_disposition))
    # Remove kepid and impute data
    df<-subset(df,select= -c(kepid))
    df<-subset(df,select= -c(kepoi_name))
    # impute missing data done before
#    temp<- preProcess(df, method = "knnImpute")
#    df <- predict(temp, df)
    return(df)
}

## Called by quit
.Last <- function() {
    graphics.off() # close devices before printing
    temp<-sessionInfo()
    cat("bye...\n")
}

if (argv$verbose){
    helptext<-help(randomForest)
    print(helptext)
    quit()
}

if (file.exists(argv$ifile)){
    df <- read.csv(argv$ifile,comment="#")
} else{
    print(paste0("File ",argv$ifile," Not found"))
    quit()
}
#make.names otherwise caret::model fails
df$koi_disposition <- factor(make.names(df$koi_disposition))

# Remove kepid and impute data
#df<-removeCols(df)
#  Only use 10% of data
index <- createDataPartition(df$koi_disposition, p = .1, list = FALSE)
df <- df[ index,]
# Train/Test
index <- createDataPartition(df$koi_disposition, p = .75, list = FALSE)
kktrain <- df[ index,]
kktest  <- df[-index,]
# remove kepid and kepoi_name for training
mtrain<-removeCols(kktrain) # kepid and kepoi_name removed
mtest<-removeCols(kktest)
# Remove kepid after test
#df<-subset(df,select= -c(kepid))

# Create File names
print(paste0(modeltype," ",argv$ifile))
Fname<-gsub(".csv","",argv$ifile,modeltype)

FmodelR<-paste0(Fname,"_",modeltype,".rds")
Fmodel<-paste0(Fname,"_",modeltype,".md")
#Fpred<-paste0(Fname,"_",modeltype,"pred.csv")
Fpred<-paste0(Fname,"_",modeltype,".pred")
#Fres<-paste0("data/",modeltype,"res.csv")
Fres<-paste0("data/",modeltype,"res")
Fplot=paste0(Fname,"_",modeltype,".pdf")

start_time <- Sys.time()

#ctrl <- trainControl(## 10-fold CV
#                           method = "repeatedcv",
#                           number = 10,
#                           ## repeated ten times
#                           repeats = 10)

ctrl <- trainControl(method = "cv",  
                     number = 2,
                     selectionFunction = "best",
                     savePredictions = TRUE,
#                     classProbs = TRUE,
#                     summaryFunction = twoClassSummary
)
mymodel = caret::train(koi_disposition ~ .,
                       data =mtrain,
                       method = modeltype,
                       trControl = ctrl,
                       #ntree = 500, 
                       #tuneGrid = data.frame(mtry = 4:10)
                       #metric="ROC"
)
mymodel
sink(Fmodel)
mymodel
sink()

#caret::confusionMatrix(mypred$y_pred, mypred$y_true,positive='CONFIRMED')

#model=naiveBayes(koi_disposition ~., data=train2,laplace=1)
saveRDS(mymodel, file=FmodelR)

#if(argv$retrain){
    #do nothing
#}else{
#load(FmodelR)
#}

#tce_plnt_num<-test$tce_plnt_num
pred <- predict(mymodel, mtest, type = "raw")
pred_prob <- predict(mymodel, mtest, type = "prob")
#labels<-test$koi_disposition
#y_true = c(test$koi_disposition)

# Package results
mypred <- data.frame(
    kepid=c(kktest$kepid),
    tce_plnt_num=c(kktest$tce_plnt_num),
    kepoi_name=kktest$kepoi_name,
    y_true=kktest$koi_disposition,
#    y_true=actual,
    y_pred = pred,
    pCANDIDATE = round(pred_prob[ , 1],2),
    pCONFIRMED = round(pred_prob[ , 2],2),
    pFALSE.POSITIVE = round(pred_prob[ , 3],2)
)

#matrix = caret::confusionMatrix(mypred$y_pred, mypred$y_true,positive='FALSE.POSITIVE')
matrix = caret::confusionMatrix(mypred$y_pred, mypred$y_true)

write.csv(mypred, file = Fpred, row.names=FALSE)

# Append results 
myresults<-resultTable(mypred,Fres) # Save results to  Fpred

myroc <- roc(mypred$y_true,mypred$pCANDIDATE)
#myroc <- roc(mypred$y_true,mypred$pCANDIDATE,levels=c("CONFIRMED", "FALSE.POSITIVE"))
myroc <- multiclass.roc(mypred$y_true,mypred$pCANDIDATE)

responses=mypred$y_true
predictor=mypred$pCANDIDATE
multiclass.roc(responses, predictor, levels = c("CONFIRMED","CANDIDATE", "FALSE.POSITIVE"))
roc.multi <- multiclass.roc(responses,predictor)
rs <- roc.multi[['rocs']]
plot.roc(rs[[1]])
sapply(2:length(rs),function(i) lines.roc(rs[[i]],col=i))
roc.multi

#plot(myroc, main="ROC curve Planetary Candidate",col="blue",lwd = 2,legacy.axes=TRUE)
#pdf(Fplot,pdf)
#plot(myroc, main="ROC curve Planetary Candidate",col="blue",lwd = 2,legacy.axes=TRUE)
#dev.off()
#print(paste0(Fname," ",FmodelR," ",Fpred," ",Fres, " ", Fplot))
cat(Fname," Base Name\n",
    Fmodel,"model file\n",
    FmodelR,"model file (rds)\n",
    Fpred,"Predicted Results file\n",
    Fres, "Append main results\n",
    Fplot, "ROC curve\n")
quit()
