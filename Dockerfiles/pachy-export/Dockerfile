FROM nikshv/p-alp-base:1.0

LABEL base="nikshv/p-alp-base:1.0"
LABEL version="1.0"
LABEL description="Exporting data from pachyderm pipeline image"

MAINTAINER Shvetsov Nikita <shvetsov.nikita@uit.no>
RUN apk add --no-cache bash openssh sshpass

COPY export.sh /tools

ENTRYPOINT ["/bin/bash"]
