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
#    results <- data.frame(actual_type = labels,
#                          predict_type = pred,
#                          prob_fp = round(pred_prob[ , 2],2),
#                          prob_pc = round(pred_prob[ , 1],2))
#    return(results)
#}

# Create Fpred based on confusion matrix or add line of results
resultTable <- function(mypred,Fres) {
    results<-caret::confusionMatrix(mypred$actual_type,mypred$predict_type)
#    print(
#        results,
#        mode = results$everything,
#        digits = max(2, getOption("digits") - 2),
#    )
#    results<-confusionMatrix(mypred$actual_type,mypred$predict_type)
    overall<-overall<-round(as.matrix(results, what = "overall"),2)
    classes<-classes<-round(as.matrix(results, what = "classes"),2)
    # AUC
    myroc <- roc(mypred$actual_type,mypred$prob_pc)
#    Auc=auc(myroc)
    end_time <- Sys.time()
    model_time<-as.numeric(round(difftime(end_time, start_time,units="secs"),3))
    df<-data.frame(ifile=c(Fname),
                   Accuracy=c(overall["Accuracy",1]),
#                   Accuracy=c(round(overall["Accuracy",1]),
                   Auc=auc(myroc),
                   Kappa=c(overall["Kappa",1]),
                   F1=c(classes["F1",1]),
                   mtime_sec=c(model_time)
                   #Sensitivity =c(classes["Sensitivity",1]),
    )
    
#    cat("Write file", file)
    # If file alreay exists append else create
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

## mmpreprocess - impute missing data is already done
# but just in case
mmpreprocess <- function(df) {
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
#    TCE2 <- read.csv(argv$ifile)
    df <- read.csv(argv$ifile)
} else{
    print(paste0("File ",argv$ifile," Not found"))
    quit()
}
#make.names otherwise caret::model fails
df$koi_disposition <- factor(make.names(df$koi_disposition))
# read and train/test
#df<- data.frame(TCE2)

# Remove kepid and impute data
#df<-mmpreprocess(df)
#  Only use 10% of data
index <- createDataPartition(df$koi_disposition, p = .1, list = FALSE)
df <- df[ index,]
# Train/Test
index <- createDataPartition(df$koi_disposition, p = .75, list = FALSE)
kktrain <- df[ index,]
kktest  <- df[-index,]
# remove kepid and kepoi_name
mtrain<-mmpreprocess(kktrain) # kepid and kepoi_name removed
mtest<-mmpreprocess(kktest)
# Remove kepid after test
#df<-subset(df,select= -c(kepid))

# Create File names
print(paste0(modeltype," ",argv$ifile))
Fname<-gsub(".csv","",argv$ifile,modeltype)
FmodelR<-paste0(Fname,modeltype,".rds")
Fmodel<-paste0(Fname,modeltype,".md")
Fpred<-paste0(Fname,modeltype,"pred.csv")
Fres<-paste0("data/",modeltype,"res.csv")
Fplot=paste0(Fname,modeltype,".pdf")

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
                       #                       metric="ROC"
)
mymodel
sink(Fmodel)
mymodel
sink()

#model=naiveBayes(koi_disposition ~., data=train2,laplace=1)
saveRDS(mymodel, file=FmodelR)

#tce_plnt_num<-test$tce_plnt_num
pred <- predict(mymodel, mtest, type = "raw")
pred_prob <- predict(mymodel, mtest, type = "prob")
#labels<-test$koi_disposition
#actual_type = c(test$koi_disposition)

#actual_type = labels,
# Package predictions
#actual=kktest$koi_disposition

mypred <- data.frame(
    kepid=c(kktest$kepid),
    tce_plnt_num=c(kktest$tce_plnt_num),
    kepoi_name=c(kktest$kepoi_name),
    actual_type=kktest$koi_disposition,
#    actual_type=actual,
    predict_type = pred,
    prob_fp = round(pred_prob[ , 2],2),
    prob_pc = round(pred_prob[ , 1],2))

write.csv(mypred, file = Fpred, row.names=FALSE)

# Append results 
myresults<-resultTable(mypred,Fres) # Save results to  Fpred

myroc <- roc(mypred$actual_type,mypred$prob_pc)
pdf(Fplot,pdf)
plot(myroc, main="ROC curve Planetary Candidate",col="blue",lwd = 2,legacy.axes=TRUE)
dev.off()
#print(paste0(Fname," ",FmodelR," ",Fpred," ",Fres, " ", Fplot))
cat(Fname,".csv Original file -\n",
    Fmodel,"model file\n",
    FmodelR,"model file (rds)\n",
    Fpred,"Predicted Results file\n",
    Fres, "Append main results\n",
    Fplot, "ROC curve\n")
quit()
