# PROTOTYPE FOR TRIMMOMATIC
import sys
from os import walk, path, sep, makedirs
import subprocess
import logging
import argparse

PROGRAMCMD = 'java -jar /tools/trimmomatic/trimmomatic'
PROGRAM = 'trimmomatic'
LOG_PATH = '/pfs/out'

################################ Util functions
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

logging.basicConfig(filename = f"{LOG_PATH}/{PROGRAM}.log", level = logging.DEBUG, format = "%(levelname)s : %(asctime)s - %(message)s")
logger = logging.getLogger()

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input folder", required=True)
    parser.add_argument("-o", "--output", help="Output folder", default=LOG_PATH)
    parser.add_argument("-m", "--mode", help="Single | paired ends (SE | PE) samples", choices=['SE', 'PE'], required=True)
    parser.add_argument("-q", "--quality", help="Quality score -phred33/-phred64", choices=['-phred33', '-phred64'], required=True)
    parser.add_argument("-c", "--adapter", help="Clipping adapter and parameters info", required=True)
    # parser.add_argument("-z", "--gzip", help="Zip results", action='store_true')
    parser.add_argument("-z", "--gzip", help="Should results be compressed with gzip?", type=bool, default=True)
    parser.add_argument("-a", "--add", help="Additional arguments")
    args = parser.parse_args()

except Exception as e:
    logger.error(e)
    sys.exit(1)

INPUTF = path.normpath(args.input) + sep
OUTPUTF = path.normpath(args.output) + sep
MODE = args.mode
QUALITY = args.quality
ADAPTER = args.adapter
#ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
#ILLUMINACLIP:./trimmomatic/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
ADD = args.add if args.add != None else ''

# Result file endings
END = '_trimmed.fastq'
if args.gzip : END += '.gz'

# Ensure about output folder
if not path.exists(OUTPUTF):
    # OUTPUTF = OUTPUTF + PREFIX + sep
    makedirs(OUTPUTF)

logger.info(f"""Preparing Trimmomatic with
mode - {MODE}
quality - {QUALITY}
input folder - {INPUTF}
output folder - {OUTPUTF}
adapter - {ADAPTER}""")
if (ADD != ''): logger.info(f"Additional arguments: {ADD}")

if MODE == 'SE':
    logger.info("Single-end mode")

    file_names = []
    paths = []
    for (dirpath, dirnames, filenames) in walk(INPUTF):
        file_names.extend(filenames)
        paths.append(dirpath)
        break

    input_ext = (".fastq", ".fastq.gz") # Filter only fastq files
    file_names = filter(lambda x:x.endswith(input_ext), file_names)

    if (len(file_names) == 0):
        logger.warning(f"No input files detected with given parameters: {args.input}")
        sys.exit(1)

    # List of full file paths
    path_files = [path.normpath(y+x) for x in file_names for y in paths]

    # Executing commands for each file
    for input_file in path_files:
        if (path.exists(input_file)):
            output_file = path.splitext(path.splitext(OUTPUTF + path.basename(input_file))[0])[0] + END
            cmd = f"{PROGRAMCMD} {MODE} {' '.join(ADD)} {QUALITY} {input_file} {output_file} {ADAPTER}"
            logger.info(f"Executing: {str((cmd.strip()).split())}")
            subprocess.call((cmd.strip()).split())
        else:
            logger.warning(f"Check that input file exsists. Skipping input - {input_file}")

elif (MODE == 'PE'):
    logger.info("Paired-end mode")

    file_names = []
    paths = []
    for (dirpath, dirnames, filenames) in walk(INPUTF):
        file_names.extend(filenames)
        paths.append(dirpath)
        break

    input_ext = (".fastq", ".fastq.gz") # Filter only fastq files
    file_names = filter(lambda x:x.endswith(input_ext), file_names)

    if (((len(file_names))%2 != 0) or (len(file_names) == 0)):
        logger.warning(f"No input files detected with given parameters: {args.input}")
        sys.exit(1)

    # Form pairs of full file paths
    path_files = [path.normpath(y+x) for x in file_names for y in paths]
    path_files = formPairsFromList(path_files)

    # Executing commands for each pair
    for input_pair in path_files:
        if (path.exists(input_pair[0]) and path.exists(input_pair[1])):
            output_file = path.splitext(path.splitext(OUTPUTF + path.basename(input_pair[0]))[0])[0] + END
            cmd = f"{PROGRAMCMD} {MODE} {' '.join(ADD)} {QUALITY} {input_pair[0]} {input_pair[1]} -baseout {output_file} {ADAPTER}"
            logger.info(f"Executing: {str((cmd.strip()).split())}")
            subprocess.call((cmd.strip()).split())
        else:
            logger.warning(f"Check that input file exsists. Skipping input - {input_file}")

else:
    logger.warning(f"There is no such mode for trimmomatic: {args.mode}")
    sys.exit(1)

logger.info("Done current datum")
logging.shutdown()
