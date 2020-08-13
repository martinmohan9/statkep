#!/usr/bin/env Rscript
# naive Bayes
oldw <- getOption("warn")
options(warn = -1)
suppressPackageStartupMessages(library("randomForest"))
suppressPackageStartupMessages(library("caret"))
#suppressPackageStartupMessages(library("e1071"))
suppressPackageStartupMessages(library("tidyverse"))
suppressPackageStartupMessages(library("argparse"))
suppressPackageStartupMessages(library("pROC"))
suppressPackageStartupMessages(library("dplyr"))

parser <- ArgumentParser(description="Calculate naive Bayes AUC, Accuracy etc.. DV=koi_disposition")
parser$add_argument("-v", "--verbose", action="store_true", default=FALSE,
                    help="verbose help [default %(default)s]")
#parser$add_argument("-r", "--retrain", action="store_true", default=TRUE,
#                    help="retrain models [default %(default)s]")
parser$add_argument("-i","--ifile", default="data/TCE1.csv",
                    help="data to be tested - several results files are created [default %(default)s]")
argv <- parser$parse_args()

set.seed(18191339)
outf <- function(data,fname,comment,rownames=FALSE) {
    write.csv(data, file = fname, row.names = rownames)
    print(paste0("Output: ", comment, " ",fname))
}

# Get prediction structure predicted number and probability
getpred <- function(model,test) {
    labels=test$koi_disposition
    pred <- predict(model, test, type = "raw")
    pred_prob <- predict(model, test, type = "prob")

    results <- data.frame(actual_type = labels,
                          predict_type = pred,
                          prob_fp = round(pred_prob[ , 2],2),
                          prob_pc = round(pred_prob[ , 1],2))
    return(results)
}

# Create resfile based on confusion matrix or add line of results
ResultTable <- function(nbpred,nbres) {
    results<-confusionMatrix(nbpred$actual_type,nbpred$predict_type)
    overall<-as.matrix(results, what = "overall")
    classes<-as.matrix(results, what = "classes")
    # AUC
    nbroc <- roc(nbpred$actual_type,nbpred$prob_pc)
    Auc=auc(nbroc)
    end_time <- Sys.time()
    model_time<-as.numeric(round(difftime(end_time, start_time,units="secs"),3))

    df<-data.frame(ifile=c(fname),
                   Accuracy=c(overall["Accuracy",1]),
                   Auc=auc(nbroc),
                   Kappa=c(overall["Kappa",1]),
                   F1=c(classes["F1",1]),
                   mtime_sec=c(model_time)
                   #mtime_sec<-as.numeric(round(difftime(Sys.time(), start_time,units="secs"),3))
                   #AccuracyPValue=c(overall["AccuracyPValue",1]),
                   #McnemarPValue=c(overall["McnemarPValue",1]),
                   #Sensitivity =c(classes["Sensitivity",1]),
                   #Specificity =c(classes["Specificity",1]),
                   #Precision=c(classes["Precision",1]),
                   #Recall=c(classes["Recall",1]),
                   #Detection_Prevalence=c(classes["Detection Prevalence",1]),
                   #Balanced_Accuracy=c(classes["Balanced Accuracy",1]),
                   )

    # If file alreay exists append else create
    if(file.exists(nbres)){
        write.table(format(df, digits=3),nbres, sep = ",",row.names=FALSE, col.names = FALSE, append = T)
    } else{
        write.csv(df, file = nbres, row.names=FALSE)
    }
    # Sort and remove duplicates
    df<- read.csv(nbres)
    df<-arrange(df,desc(Accuracy)) # sort by Accuracy
    df[!duplicated(df), ] # remove duplicates
    df[!duplicated(df$Accuracy), ] # remove dup accuracy?
    write.table(format(df, digits=3),nbres, sep = ",",row.names=FALSE, col.names=TRUE, append = FALSE)
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
    TCE2 <- read.csv(argv$ifile)
} else{
    print(paste0("File ",argv$ifile," Not found"))
    quit()
}
# read and train/test
df<- data.frame(TCE2)
df$koi_disposition <- factor(df$koi_disposition)
#index <- sample(1:dim(df)[1], dim(df)[1] * .75, replace=FALSE)
#train <- df[index, ]
#test <- df[-index, ]

# Remove kepid and impute data
df<-subset(df,select= -c(kepid))
temp<- preProcess(df, method = "knnImpute")
df <- predict(temp, df)
# Train/Test
index <- createDataPartition(df$koi_disposition, p = .75, list = FALSE)
train <- df[ index,]
test  <- df[-index,]

# name  result files
modeltype="rf"
print(paste0(modeltype," ",argv$ifile))
fname<-gsub(".csv","",argv$ifile,modeltype)
modelfile<-paste0(fname,modeltype,".rds")
resfile<-paste0(fname,modeltype,"res.csv")
nbres<-paste0("data/",modeltype,"res.csv")
plotname=paste0(fname,modeltype,".pdf")
print(paste0(fname," ",modelfile," ",resfile," ",nbres, " ", plotname))
start_time <- Sys.time()

#ctrl <- trainControl(## 10-fold CV
#                           method = "repeatedcv",
#                           number = 10,
#                           ## repeated ten times
#                           repeats = 10)

ctrl <- trainControl(method = "cv",  number = 2)
mymodel = caret::train(koi_disposition ~ ., data = train,  method = modeltype,trControl = ctrl)
# model
#model=naiveBayes(koi_disposition ~., data=train,laplace=1)
saveRDS(mymodel, file=modelfile)

labels<-test$koi_disposition
pred <- predict(mymodel, test, type = "raw")
pred_prob <- predict(mymodel, test, type = "prob")

# Package predictions
nbpred <- data.frame(actual_type = labels,
                     predict_type = pred,
                     prob_fp = round(pred_prob[ , 2],2),
                     prob_pc = round(pred_prob[ , 1],2))
write.csv(nbpred, file = resfile, row.names=TRUE)

nbroc <- roc(nbpred$actual_type,nbpred$prob_pc)

# Append results 
nbresults<-ResultTable(nbpred,nbres) # Save results to  resfile

#plotname=paste0(resfile,".pdf")
pdf(plotname,pdf)
plot(nbroc, main="ROC curve for Planetary Candidate finder",col="blue",lwd = 2,legacy.axes=TRUE)
dev.off()
cat(paste0(fname,".csv Original file\n",modelfile," model file\n",resfile," Predicted Results file\n",nbres, " Append main results here \n", plotname, " ROC curve\n"))
quit()
