# PROTOTYPE FOR FASTQC
import sys
from os import walk, path, sep, makedirs
import subprocess
import logging
import argparse

PROGRAM = 'fastqc'
LOG_PATH = '/pfs/out'

logging.basicConfig(filename = f"{LOG_PATH}/{PROGRAM}.log",
                    level = logging.DEBUG,
                    format = "%(levelname)s : %(asctime)s - %(message)s")
logger = logging.getLogger()

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input folder", required=True)
    parser.add_argument("-o", "--output", help="Output folder", default=LOG_PATH)
    parser.add_argument("-a", "--add", help="Additional arguments")
    args = parser.parse_args()

except Exception as e:
    logger.error(e)
    sys.exit(1)

INPUTF = path.normpath(args.input) + sep
OUTPUTF = path.normpath(args.output) + sep
ADD = args.add if args.add != None else ''

# Ensure about output folder
if not path.exists(OUTPUTF):
    # OUTPUTF = OUTPUTF + PREFIX + sep
    makedirs(OUTPUTF)

logger.info(f"Preparing FastQC with input folder - {INPUTF} & output folder - {OUTPUTF}")
if (ADD != ''): logger.info(f"Additional arguments: {ADD}")

file_names = []
paths = []
for (dirpath, dirnames, filenames) in walk(INPUTF):
    file_names.extend(filenames)
    paths.append(dirpath)
    break # Need only 1 level of depth
    # root, directories, filenames
    # for directory in directories:
    #     print (path.join(root, directory))
    # for filename in filenames:
    #     print (path.join(root,filename))

input_ext = (".fastq", ".fastq.gz") # Filter only fastq files
file_names = list(filter(lambda x:x.endswith(input_ext), file_names))

if (len(file_names) == 0):
    logger.warning(f"No input files detected with given parameters: {args.input}")
    sys.exit(1)

# List of full file paths
path_files = [path.normpath(y+x) for x in file_names for y in paths]

# Executing commands for each file
for input_file in path_files:
    if (path.exists(input_file)):
        cmd = f"{PROGRAM} -o {OUTPUTF} {input_file} {ADD}"
        logger.info(f"Executing: {str((cmd.strip()).split())}")
        subprocess.call((cmd.strip()).split())
    else:
        logger.warning(f"Check that input file exsists. Skipping input - {input_file}")

logger.info("Done current datum")
logging.shutdown()
