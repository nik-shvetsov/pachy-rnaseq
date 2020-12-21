source("https://bioconductor.org/biocLite.R")
biocLite("BiocGenerics")
biocLite("ensembldb")
biocLite("EnsDb.Hsapiens.v86")
biocLite("DESeq2")
biocLite("tximport")

library('devtools')
install('/install_scripts/EnsDb.Hsapiens.v92')
