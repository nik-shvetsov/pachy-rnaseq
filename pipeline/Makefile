check-pachctl:
	pachctl version

create-input-repos: check-pachctl
	pachctl create-repo input-${id}
	pachctl create-repo input_transcr_grch38_v86-${id}

clean-pipelines: check-pachctl
	pachctl delete-pipeline tximport-${id}
	pachctl delete-pipeline salmon_quant-${id}
	pachctl delete-pipeline salmon_idx-${id}
	pachctl delete-pipeline fastqc_post-${id}
	pachctl delete-pipeline trimmomatic-${id}
	pachctl delete-pipeline fastqc_pre-${id}
	pachctl delete-repo input_transcr_grch38_v86-${id}
	pachctl delete-repo input-${id}

create-pipelines: check-pachctl
	pachctl create-pipeline -f fastqc_pre-${id}.json
	pachctl create-pipeline -f trimmomatic-${id}.json
	pachctl create-pipeline -f fastqc_post-${id}.json
	pachctl create-pipeline -f salmon_idx-${id}.json
	pachctl create-pipeline -f salmon_quant-${id}.json
	pachctl create-pipeline -f tximport-${id}.json

update-pipelines: check-pachctl
	pachctl update-pipeline -f fastqc_pre-${id}.json --reprocess
	pachctl update-pipeline -f trimmomatic-${id}.json --reprocess
	pachctl update-pipeline -f fastqc_post-${id}.json --reprocess
	pachctl update-pipeline -f salmon_idx-${id}.json --reprocess
	pachctl update-pipeline -f salmon_quant-${id}.json --reprocess
	pachctl update-pipeline -f tximport-${id}.json --reprocess

fill-repos: check-pachctl
	pachctl put-file input_transcr_grch38_v86-${id} master Homo_sapiens.GRCh38.cdna.all.fa.gz -f /mnt/scratch/data/fasta/grch38_v86/Homo_sapiens.GRCh38.cdna.all.fa.gz
	pachctl put-file -r input-${id} master / -f /mnt/scratch/data/projects/${proj}/fastq/
	sleep 10
	pachctl list-job

create-all: check-pachctl create-input-repos fill-repos create-pipelines
	@echo "Done."
