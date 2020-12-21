# PROTOTYPE FOR TXIMPORT
import sys
from os import walk, path, sep, makedirs
import subprocess
import logging
import argparse

PROGRAM = "tximport"
SCRIPT_NAME = "tximport.R"
COMMAND_R = "Rscript"
LOG_PATH = '/pfs/out'

logging.basicConfig(filename = f"{LOG_PATH}/{PROGRAM}.log",
                    level = logging.DEBUG,
                    format = "%(levelname)s : %(asctime)s - %(message)s")
logger = logging.getLogger()

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input folder", required=True)
    parser.add_argument("-o", "--output", help="Output folder", default=LOG_PATH)
    parser.add_argument("-e", "--enspver", help="Version of ensemblDB package used for identifying genes (v92 default)", choices=['v86','v92'], default="v92")
    args = parser.parse_args()

except Exception as e:
    logger.error(e)
    sys.exit(1)

INPUTF = path.normpath(args.input) + sep
OUTPUTF = path.normpath(args.output) + sep
ENSDB_VERSION = args.enspver

# Ensure about output folder
if not path.exists(OUTPUTF):
    # OUTPUTF = OUTPUTF + '_' + PROGRAM + sep
    makedirs(OUTPUTF)

logger.info(f"""Preparing tximport script with
input folder - {INPUTF}
output folder - {OUTPUTF}
ensDB version - {ENSDB_VERSION}""")

if (path.exists(INPUTF) and path.exists(OUTPUTF)):
    cmd = f"{COMMAND_R} {SCRIPT_NAME} {INPUTF} {OUTPUTF} {ENSDB_VERSION}"
    # Rscript tximport.R {input_folder} {output_folder} {v86}
    logger.info(f"Executing: {str((cmd.strip()).split())}")
    subprocess.call((cmd.strip()).split())
else:
    logger.warning(f"Check the existence of the provided input folder: {args.input}")
    sys.exit(1)

logger.info("Done current datum")
logging.shutdown()
