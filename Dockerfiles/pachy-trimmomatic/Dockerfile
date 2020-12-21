FROM nikshv/p-base:3.7

LABEL base="p-base"
LABEL version="3.7"
LABEL software="Trimmomatic"
LABEL software.version="0.38"
LABEL description="A flexible read trimming tool for Illumina NGS data."
LABEL website="http://www.usadellab.org/cms/?page=trimmomatic/"
LABEL documentation="http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf"
LABEL license="https://www.gnu.org/copyleft/gpl.html"

MAINTAINER Shvetsov Nikita <shvetsov.nikita@uit.no>

ENV VER=0.38
ENV URL=http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic
ENV ZIP=Trimmomatic-$VER.zip

RUN wget $URL/$ZIP && \
	unzip $ZIP && \
	mv Trimmomatic-$VER trimmomatic && \
	mv trimmomatic/trimmomatic-$VER.jar trimmomatic/trimmomatic && \
	rm $ZIP

COPY trimmomatic.py /tools

ENTRYPOINT ["java", "-jar","/tools/trimmomatic/trimmomatic"]
