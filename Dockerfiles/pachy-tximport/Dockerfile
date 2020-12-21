FROM nikshv/p-r-base:3.5

LABEL base="p-r-base:3.5"
LABEL software="R-tximport"
LABEL software.version="1.10.0"
LABEL description="R environment for processing quantification data with tximport library"
LABEL website="http://bioconductor.org/packages/release/bioc/html/tximport.html"
LABEL documentation="http://bioconductor.org/packages/release/bioc/vignettes/tximport/inst/doc/tximport.html"
LABEL licence="https://www.r-project.org/Licenses/"

MAINTAINER Shvetsov Nikita <shvetsov.nikita@uit.no>

RUN mkdir /install_scripts
COPY install.R /install_scripts/install.R
COPY EnsDb.Hsapiens.v92.tar.gz /install_scripts/EnsDb.Hsapiens.v92.tar.gz
RUN tar -zxvf /install_scripts/EnsDb.Hsapiens.v92.tar.gz && mv EnsDb.Hsapiens.v92 /install_scripts/ && \
	Rscript /install_scripts/install.R && rm -rf /install_scripts

COPY ./scripts/* /tools
COPY tximport.py /tools

ENTRYPOINT ["R"]
