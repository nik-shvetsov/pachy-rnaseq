id=$1
user=$2
server=$3
projectpath=$4

mkdir ${id}-export
# Gather results from tximport repo
cp -r ${id}-tximport/master/ ./${id}-export/

# Gather logs
cp ${id}-fastq_pre/master/fastqc.log ./${id}-export/fastqc_pre.log
cp ${id}-trimmomatic/master/trimmomatic.log ./${id}-export/trimmomatic.log
cp ${id}-trimmomatic/master/fastqc.log ./${id}-export/fastqc_post.log
cp ${id}-trimmomatic/master/salmon.log ./${id}-export/salmon_idx.log
cp ${id}-trimmomatic/master/salmon.log ./${id}-export/salmon_quant.log
cp ${id}-trimmomatic/master/tximport.log ./${id}-export/tximport.log

# Zip results
tar -zcvf ${id}-export.tar.gz ${id}-export/

# Copy to server
sshpass -p ${PASS} scp ${id}-export.tar.gz $user@$server:$projectpath

# Init git repo
sshpass -p ${PASS} ssh -o StrictHostKeyChecking=no ${user}@${server} 'cd ${projectpath}; tar -zxf ${id}-export.tar.gz; rm -rf ${id}-export.tar.gz; git init; git add .; git commit -m"Initial commit"; git status'

