# PROTOTYPE FOR SALMON
import sys
from os import walk, path, sep, makedirs
import subprocess
import logging
import argparse

PREFIX = 'salmon_'
PROGRAM = 'salmon'
LOG_PATH = '/pfs/out'

################################ Util functions
def getFilesAndPaths(input_folder):
    file_names = []
    paths = []
    for (dirpath, dirnames, filenames) in walk(input_folder):
        file_names.extend(filenames)
        paths.append(dirpath)
        break
    return (file_names, paths)

def formPairsFromList(lst):
    if len(lst)%2 == 0:
        lst.sort()
        tlst = []
        for idx in range(0,len(lst),2):
            tpl = (lst[idx], lst[idx+1])
            tlst.append(tpl)
        return tlst
    else:
        return
################################

logging.basicConfig(filename = f"{LOG_PATH}/{PROGRAM}.log",
                    level = logging.DEBUG,
                    format = "%(levelname)s : %(asctime)s - %(message)s")
logger = logging.getLogger()

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input folder", required=True)
    parser.add_argument("-o", "--output", help="Output folder", default=LOG_PATH)
    parser.add_argument("-m", "--mode", help="index or quant mode of salmon", choices=['index', 'quant'], required=True)
    parser.add_argument("-a", "--add", help="Additional arguments")
    args, _ = parser.parse_known_args()
    if (args.mode == 'quant'):
        parser.add_argument("-x", "--idx", help="Folder, containing index info", required=True)
        parser.add_argument("-l", "--library", help="Library type (A - auto - is by default)", default='A')
        parser.add_argument("-r", "--readtype", help="single | paired reads", choices=['single', 'paired'], required=True)
        args = parser.parse_args()

except Exception as e:
    logger.error(e)
    sys.exit(1)

INPUTF = path.normpath(args.input) + sep
OUTPUTF = path.normpath(args.output) + sep
MODE = args.mode
ADD = args.add if args.add != None else ''

#salmon index -t transcripts.fa -i transcripts_index --type quasi -k 31
#salmon quant -i transcripts_index -l <LIBTYPE> -r reads.fq -o transcripts_quant
#salmon quant -i transcripts_index -l <LIBTYPE> -1 reads1.fq -2 reads2.fq -o transcripts_quant
#salmon quant -t transcripts.fa -l <LIBTYPE> -a aln.bam -o salmon_quant

# Ensure about output folder
if not path.exists(OUTPUTF):
    # OUTPUTF = OUTPUTF + PREFIX + sep
    makedirs(OUTPUTF)

if MODE == 'index':
    PREFIX += 'idx'
if MODE == 'quant':
    PREFIX += 'quant'

logger.info(f"""Preparing Salmon with
mode - {MODE}
input folder - {INPUTF}
output folder - {OUTPUTF}""")
if (ADD != ''): logger.info(f"Additional arguments: {ADD}")

if MODE == 'index':
    logger.info("Indexing transcriptome")

    file_names, paths = getFilesAndPaths(INPUTF)

    input_ext = (".fa", ".fa.gz") # Filter only fa files
    file_names = filter(lambda x:x.endswith(input_ext), file_names)

    if (len(file_names) == 0):
        logger.warning(f"No input files detected with given parameters: {args.input}")
        sys.exit(1)

    # List of full file paths
    path_files = [path.normpath(y+x) for x in file_names for y in paths]

    # Executing commands for each file
    for input_file in path_files:
        if (path.exists(input_file)):
            #output_file = path.splitext(path.splitext(OUTPUTF + path.basename(input_file))[0])[0] + '_idx'
            cmd = f"{PROGRAM} {MODE} -t {input_file} -i {OUTPUTF} {' '.join(ADD)}"
            #salmon index -t transcripts.fa -i transcripts_index --type quasi -k 31
            logger.info(f"Executing: {str((cmd.strip()).split())}")
            subprocess.call((cmd.strip()).split())
        else:
            logger.warning(f"Check that input file exsists. Skipping input - {input_file}")

elif (MODE == 'quant'):
    logger.info("Quasi-quantification")

    # Division on single-read or paired-read

    # Identify transcripts or index folder
    TRS_OR_INDEX = args.idx
    TRANSCRIPT_ARGS = [TRS_OR_INDEX]

    if TRS_OR_INDEX.lower().endswith('.fa') or TRS_OR_INDEX.lower().endswith('fa.gz'):
        TRANSCRIPT_ARGS.insert(0,'-t')
    else:
        TRANSCRIPT_ARGS.insert(0,'-i')
    TRANSCRIPT_ARGS = ' '.join(TRANSCRIPT_ARGS)

    # Lib type
    LIBTYPE = args.library
    LIBTYPE_ARGS = ' '.join(['-l', LIBTYPE])

    # 'single' - single read | 'paired' - paired read
    READ_MODE = args.readtype

    # Process input files
    file_names, paths = getFilesAndPaths(INPUTF)

    if READ_MODE == 'single':

        input_ext = (".fastq", ".fastq.gz", ".bam", ".bam.gz", ".fq", ".fq.gz") # Filter only fastq and bam files
        file_names = filter(lambda x:x.endswith(input_ext), file_names)

        if (len(file_names) == 0):
            logger.warning(f"No input files detected with given parameters: {args.input}")
            sys.exit(1)

        logger.info("Single-read mode")

        # List of full file paths
        path_files = [path.normpath(y+x) for x in file_names for y in paths]

        # Executing commands for each file
        for input_file in path_files:
            if (path.exists(input_file)):
                if path.splitext(input_file)[1] == '.bam' or path.splitext(input_file)[1] == '.bam.gz':
                    INPUTFILE_ARGS = ' '.join(['-a', input_file])
                else:
                    INPUTFILE_ARGS = ' '.join(['-r', input_file])
                #output_file = path.splitext(path.splitext(OUTPUTF + path.basename(input_file))[0])[0] + '_quant' + sep
                OUTPUTFILE_ARGS = ' '.join(['-o', path.splitext(path.splitext(OUTPUTF + path.basename(input_file))[0])[0] + '_quant'])
                cmd = f"{PROGRAM} {MODE} {TRANSCRIPT_ARGS} {LIBTYPE_ARGS} {INPUTFILE_ARGS} {OUTPUTFILE_ARGS} {' '.join(ADD)}"
                #salmon quant -i {transcript.folder} -l {LIBTYPE} -r {input_file} -o {output_path+output_file}
                #salmon quant -t {transcripts.folder} -l {LIBTYPE} -a {input_file(bam)} -o {output_path+output_file}
                logger.info(f"Executing: {str((cmd.strip()).split())}")
                subprocess.call((cmd.strip()).split())
            else:
                logger.warning(f"Check that input file exsists. Skipping input - {input_file}")


    elif READ_MODE == 'paired':

        input_ext = (".fastq", ".fastq.gz", ".fq", ".fq.gz") # Filter only fastq and bam files
        file_names = filter(lambda x:x.endswith(input_ext), file_names)

        if (((len(file_names))%2 != 0) or (len(file_names) == 0)):
            logger.warning(f"No input files detected with given parameters: {args.input}")
            sys.exit(1)

        logger.info("Paired-read mode")

        # Form pairs of full file paths
        path_files = [path.normpath(y+x) for x in file_names for y in paths]
        path_files = formPairsFromList(path_files)

        # Executing commands for each pair
        for input_pair in path_files:
            if (path.exists(input_pair[0]) and path.exists(input_pair[1])):
                INPUTFILE_ARGS = ' '.join(['-1', input_pair[0], '-2', input_pair[1]])
                #output_file = path.splitext(path.splitext(OUTPUTF + path.basename(input_pair[0]))[0])[0] + '_quant' + sep
                OUTPUTFILE_ARGS = ' '.join(['-o', path.splitext(path.splitext(OUTPUTF + path.basename(input_pair[0]))[0])[0] + '_quant'])
                cmd = f"{PROGRAM} {MODE} {TRANSCRIPT_ARGS} {LIBTYPE_ARGS} {INPUTFILE_ARGS} {OUTPUTFILE_ARGS} {' '.join(ADD)}"
                #salmon quant -i transcripts_idx -l <LIBTYPE> -1 reads1.fq -2 reads2.fq -o transcripts_quant
                logger.info(f"Executing: {str((cmd.strip()).split())}")
                subprocess.call((cmd.strip()).split())
            else:
                logger.warning(f"Check that input file exsists. Skipping input - {input_pair}")

else:
    logger.warning(f"There is no such mode for salmon: {args.mode}")
    sys.exit(1)

logger.info("Done current datum")
logging.shutdown()
