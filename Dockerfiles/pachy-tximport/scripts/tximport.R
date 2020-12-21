#0. Arguments
# library(optparse)
#
# option_list = list(
#   make_option(c("-i", "--input"), action="store", default=NA, type='character',
#               help="Salmon data folder"),
#   make_option(c("-o", "--output"), action="store", default=NA, type='character',
#               help="Output folder"),
#   make_option(c("-e", "--enspver"), action="store", default=NA, type='character',
#               help="ensembldb HS package version")
# )
# opt = parse_args(OptionParser(option_list=option_list))

args <- commandArgs(trailingOnly = TRUE)
opt <- list()
opt$input <- args[1]
opt$output <- args[2]
opt$enspver <- args[3]

if (opt$input == NA || opt$output == NA) stop("Missing input or output arguments!")
# if (opt$enspver == NA) opt$enspver <- 'v86'
salmon_output_folder <- opt$input
out_count <- gsub("//","/",file.path(opt$output, "counts.rds"))
out_rds <- gsub("//","/",file.path(opt$output, "txi.rds"))
out_abund <- gsub("//","/",file.path(opt$output, "abundance.rds"))
out_rlog <- gsub("//","/",file.path(opt$output, "rlog.rds"))
# file.path("/pfs/out","counts_result.csv")

gtf_version <- opt$enspver
# gtf_file <- gsub("//","/",file.path(gtf_folder, list.files(path = gtf_folder)[1]))

###########################################
#1. Create tx2gene dataframe

library(ensembldb)

if (gtf_version == 'v86') {
  library(EnsDb.Hsapiens.v86)
  tx <- transcripts(EnsDb.Hsapiens.v86, return.type = "DataFrame")
} else {
  library(EnsDb.Hsapiens.v92)
  tx <- transcripts(EnsDb.Hsapiens.v92, return.type = "DataFrame")
}
tx2gene <- as.data.frame(tx[,c("tx_id", "gene_id")])

###########################################
#2. Create tximport object, get csv file with counts

library(tximport)
library(DESeq2)
library(readr)
library(dplyr)

files <- c()
names <- c()

samples <- list.dirs(path = salmon_output_folder, full.names = TRUE, recursive = FALSE)
for (i in samples) {
  files <- c(files, file.path(i, "quant.sf"))
  names <- c(names, basename(i))
}

txi <- tximport(files, type = "salmon", tx2gene = tx2gene, ignoreTxVersion = TRUE)
saveRDS(txi, file = out_rds)

# Counts
counts <- as.data.frame(txi$counts)
colnames(counts) <- names
saveRDS(counts, file = out_count)

# Abundance
abundance <- as.data.frame(txi$abundance)
colnames(abundance) <- names
saveRDS(abundance, file = out_abund)

# DESeq2
coldata <- data.frame(ids=names, row.names=names)
de <- DESeqDataSetFromTximport(txi = txi, colData = coldata, design = ~1)
# counts_de <- counts(de)
data_rlog <- as.data.frame(assay(rlog(de)))
saveRDS(data_rlog, file = out_rlog)
# write.csv(data_rlog, file = out_rlog, row.names = TRUE)

###########################################
#3. Additional analisys
