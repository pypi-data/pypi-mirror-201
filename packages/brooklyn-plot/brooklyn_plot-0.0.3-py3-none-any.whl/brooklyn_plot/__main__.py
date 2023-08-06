#!/usr/bin/env python

# This is used to calculate pearson correlations of a user defined set of genes against a user defined set of targets.
# The purpose is to generate data for a Brooklyn plot - evaluating coexpression patterns in single cell datasets
# which inform on chromosomal bursting and coexpression.
# Code by Arun Patil and Marc Halushka (2022)

# Import basic packages 
from pathlib import Path
import time
import sys
import os
import pandas as pd

#Custom brooklyn libraries
from brooklyn_plot.libs.parse import parseArg
from brooklyn_plot.libs.coexpression import brooklyn_arch
from brooklyn_plot.libs.summary import summarize


def main():
    # Capture the start time
    globalstart = time.perf_counter()
    # Fetch all the arguments by users/default
    args = parseArg()
    # Read the path of the h5ad file and check if it exists if true, then get absolute path of the file
    if Path(args.h5ad).exists():
        h5file = str(Path(args.h5ad).resolve())
    else:
        print("The h5ad file provided doesn't exists. Please provide the correct file!")
        exit()
    # Read the path of the biomart file and check if it exists if true, then get absolute path of the file
    if Path(args.biomart).exists():
        annotations = str(Path(args.biomart).resolve())
    else:
        print("The gene annotations file (biomart) provided doesn't exists. Please provide the correct file!")
        exit()
    # Create output directory if it doesn't exist 
    try:
        if args.outDirName:
            ourDir_n = str(args.outDirName)
            workDir = Path(args.outDir)/ourDir_n if args.outDir else Path.cwd()/ourDir_n
    except AttributeError:
        tStamp = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
        ourDir = "brooklyn_" + tStamp
        workDir = Path(args.outDir)/ourDir if args.outDir else Path.cwd()/ourDir
    Path(workDir).mkdir(exist_ok=True, parents=True)
    # Read query gene list from a CSV file
    gl = pd.read_csv(args.query)
    geneList = gl[gl.columns[0]].values.tolist()
    # Read subject gene list from a CSV file
    agl = pd.read_csv(args.subject)
    againstList = agl[agl.columns[0]].values.tolist()
    # Create output filenames provided by user or use default values
    if args.outFile:
        fileBase = args.outFile
    else:
        fileBase = "brooklyn"
    # Get number of threads 
    threads = args.threads
    return_status = False
    # Initiating co-expression pattern finding
    return_status = brooklyn_arch(h5file, workDir, annotations, geneList, againstList, threads)
    if not return_status:
        print("Error: While finding co-expression patterns, the execution was terminated for reasons unknown!")
        exit()
    # Summarizing the overall gene co-expression and generating summary file for brooklyn_plot
    summarize(workDir, fileBase)
    RscriptDirTmp = Path(__file__).resolve().parents[0]
    RscriptDir = Path(RscriptDirTmp)/('rScripts')/('brooklynPlot.R')
    brooklynSummarySorted = Path(workDir)/str(str(fileBase) + "_sorted_summary.csv")
    outbrooklynplot = Path(workDir)/str(str(fileBase) + "_plot.pdf")
    os.system('Rscript %s %s %s'%(RscriptDir, brooklynSummarySorted, outbrooklynplot))
    globalend_time = time.perf_counter()
    print(f'\nThe path to ourput directory: {workDir}')
    print(f'\nThe analysis completed in {round(globalend_time-globalstart, 4)} second(s)\n')


# Calling main function - first function called
if __name__ == '__main__':
    main()
