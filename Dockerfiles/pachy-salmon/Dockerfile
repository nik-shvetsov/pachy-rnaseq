FROM nikshv/p-base:3.7

LABEL base="p-base"
LABEL version="3.7"
LABEL software="Salmon"
LABEL software.version="0.11.3"
LABEL description="Tool for quantifying the expression of transcripts using RNA-seq data."
LABEL website="https://combine-lab.github.io/salmon/"
LABEL documentation="http://salmon.readthedocs.io/en/latest/"
LABEL license="https://www.gnu.org/copyleft/gpl.html"

MAINTAINER Shvetsov Nikita <shvetsov.nikita@uit.no>

ENV VER=0.11.3
ENV PROG=salmon-${VER}-linux_x86_64
ENV ZIP=${PROG}.tar.gz
ENV URL=https://github.com/COMBINE-lab/salmon/releases/download/v0.11.3/${ZIP}

RUN wget $URL && \
	tar -zxf $ZIP && \
	mv $PROG salmon && \
	rm $ZIP

ENV PATH=/tools/salmon/bin:${PATH}

COPY salmon.py /tools

ENTRYPOINT ["salmon"]
