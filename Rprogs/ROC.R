#!/usr/bin/env Rscript
oldw <- getOption("warn")
options(warn = -1)

# Suppress messages in argv
suppressPackageStartupMessages(library("caret"))
#suppressPackageStartupMessages(library("tidyverse"))
suppressPackageStartupMessages(library("argparse"))

# Options by default ArgumentParser will add an help option
parser <- ArgumentParser(description="Filter multicorrelated values with pearson's R 0 to 1 --omit columns such as Dependent Variable")
parser$add_argument("-v", "--verbose", action="store_true", default=FALSE,
                    help="verbose help [default %(default)s]")
parser$add_argument("-i","--ifiles", default="data/TCE1.csv",
                    help="List of input files to create ROC curves [default %(default)s]")
parser$add_argument("--omit", default="koi_disposition,kepid,kepoi_name",
                    help="List of cols to omit [default %(default)s]")
parser$add_argument("--title", default="ROC curves",
                    help="Title to add to ROC file [default %(default)s]")
argv <- parser$parse_args()

# write output to file and tell user
outf <- function(dframe,fname,comment,rownames=FALSE) {
    write.csv(dframe, file = fname, row.names = rownames)
    print(paste0("Output: ", comment, " ",fname))
}

## Not run: ## Unix-flavour example
.Last <- function() {
    graphics.off() # close devices before printing
    temp<-sessionInfo()
    cat("bye...\n")
}

if (file.exists(argv$ifile)){
    TCE1 <- read.csv(argv$ifile)
} else{
    print(paste0("File ",argv$ifile," Not found"))
    quit()
}

# CONFIRMED and CANDIDATE combined
ifiles=unlist(strsplit(argv$files, ",")) #list of files to use for ROC


if (argv$hmap){hmap(TCE2cor,cfname)}
print(paste0("Stats: cor_all:",length(TCE1all)," ,cor=<",rmin," ",length(cormin)," ,cor>=",rmax," ",length(cormax)," ,cor removed ", length(corrlist), " ,Final Col nr ",dim(TCEomit)[2]))
quit()
