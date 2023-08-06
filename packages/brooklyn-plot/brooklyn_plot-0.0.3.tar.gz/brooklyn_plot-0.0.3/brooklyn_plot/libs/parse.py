import os
import sys
import argparse
import subprocess
from pkg_resources import get_distribution

def parseArg():
    version = get_distribution("brooklyn_plot").version
    parser = argparse.ArgumentParser(description='Brooklyn (Gene co-expression and transcriptional bursting pattern recognition tool in single cell/nucleus RNA-sequencing data)',usage='brooklyn_plot [options]',formatter_class=argparse.RawTextHelpFormatter,)
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    parser.add_argument('--version', action='version', version='%s'%(version))
    group = parser.add_argument_group("Options",description='''
-h5,   --h5ad               input file in .h5ad format (accepts .h5ad) 
-ba,   --biomart            the reference gene annotations (in .csv format) 
-od,   --outDir             the directory of the outputs (Default: brooklyn-date-hh-mm-ss) 
-of,   --outFile            the name of summarized brooklyn file as CSV file and a brooklyn plot in PDF (Default: brooklyn)
-ql,   --query              the list of genes to be queried upon (one gene per line and in .csv format)
-sl,   --subject            the list of genes to be compared with (one gene per line and in .csv format)
-cpu,  --threads            the number of processors to use for trimming, qc, and alignment (Default: 1)
''')
    group.add_argument('-h5', '--h5ad', required=True, help=argparse.SUPPRESS) 
    group.add_argument('-ba', '--biomart', required=True, help=argparse.SUPPRESS)
    group.add_argument('-od', '--outDir', help=argparse.SUPPRESS)
    group.add_argument('-of', '--outFile', help=argparse.SUPPRESS)
    group.add_argument('-ql', '--query', required=True, help=argparse.SUPPRESS)
    group.add_argument('-sl', '--subject', required=True, help=argparse.SUPPRESS)
    group.add_argument('-cpu', '--threads', type=int, default='1', help=argparse.SUPPRESS)

    return parser.parse_args()
