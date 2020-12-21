FROM nikshv/p-base:3.7

LABEL base="p-base"
LABEL version="3.7"
LABEL software="FASTQC"
LABEL software.version="0.11.8"
LABEL description="Quality control tool for high throughput sequence data."
LABEL website="http://www.bioinformatics.babraham.ac.uk/projects/fastqc/"
LABEL documentation="http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/"
LABEL license="https://www.gnu.org/copyleft/gpl.html"

MAINTAINER Shvetsov Nikita <shvetsov.nikita@uit.no>

ENV VER=0.11.8
ENV URL=http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
ENV ZIP=fastqc_v$VER.zip

RUN wget $URL/$ZIP && \
	unzip $ZIP && \
	mv FastQC fastqc && \
	rm $ZIP && \
	chmod +x fastqc/fastqc && \
	ln -s /tools/fastqc/fastqc /usr/local/bin/fastqc

COPY fastqc.py /tools

ENTRYPOINT ["fastqc"]
