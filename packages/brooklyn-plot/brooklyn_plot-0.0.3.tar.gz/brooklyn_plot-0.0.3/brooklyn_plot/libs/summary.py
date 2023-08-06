#!/usr/bin/python
# This is used to determine the percent on the same chromosome_name.
# It calculates the shared chromosome status of each gene to the top pearson correlated genes.
# This is reported for the top 50 correlated genes as a percent.  This can be used to 
# plot a Brooklyn plot across the genome.
# Code by Arun Patil and Marc Halushka (2022)

import os
import sys
import pandas as pd
import time
from pathlib import Path

def summarize(workDir, fileBase):
    globalstart = time.perf_counter()
    basepath = Path(workDir)/"cor_genes"
    brookSum = Path(workDir)/str(str(fileBase) + "_summary.csv")
    brookSumSorted = Path(workDir)/str(str(fileBase) + "_sorted_summary.csv")
    new_emptyList = list()
    for entry in os.listdir(basepath):
        if "csv" in entry:
            df = pd.read_csv(os.path.join(basepath,entry))
            sdf = df.sort_values('r', ascending=False)
            sdfp = sdf[sdf['r'] >= 0]
            try:
                sdfp2 = sdfp.nlargest(51,'r')
                df_1 = sdfp2.iloc[:1,:]
                req_chr = df_1.iloc[0]['chromosome_name']
                df_2 = sdfp2.iloc[1:,:]
                denominator = int(df_2.shape[0])
                try:
                    occurence = int(df_2['chromosome_name'].value_counts()[req_chr])
                except KeyError:
                    occurence = 0
                    #denominator = 0
                if denominator > 0:
                    percent_occurence = str(round((occurence / denominator) * 100,2))
                else:
                    percent_occurence = "0"
                base = (df_1.values.tolist())
                base = base[0] + [str(occurence), str(denominator), percent_occurence]
                new_emptyList.append(base)
            except TypeError:
                pass

    summarizedDF = pd.DataFrame(new_emptyList, columns = ['gene', 'r', 'p', 'bon', 'neg_log10_p', 'hgnc_symbol','chromosome_name', 'start_position', 'xMean', 'end_position', 'band', 'occurence', 'denominator', 'percent_occurence'])
    summarizedDF = summarizedDF.round(decimals = 2)
    summarizedDF.to_csv(brookSum, index=False)

    df2 = summarizedDF
    # Create chromosome order and sort accordingly
    chrOrder = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X', 'Y', 'M', 'MT']
    chrIndex = dict(zip(chrOrder, range(len(chrOrder)))) # Creates a dictionary of chromosomes and a serial number as value
    df2 = df2[df2['chromosome_name'].notna()] # Filter out any rows which don't represent any chromosomes (such as blank lines at the EOF)
    df2['chromosome_name'] = df2['chromosome_name'].astype('string') # Making sure the column chromosome name is a string data type
    df2 = df2.loc[df2['chromosome_name'].isin(chrOrder)] # Check for only chromosomes and avoid any patches
    df2['ChrOrder'] = df2['chromosome_name'].map(chrIndex) # Creating a new column chrOrder which defines the order of each chromosomes.
    df2['ChrOrder'] = df2['ChrOrder'].astype('int') # Making sure the column chrOrder is a integer 
    df2.sort_values(['ChrOrder', 'end_position'], ascending = True, inplace = True) # Sort based on chromosome order and end position of each gene 
    df2.drop(columns='ChrOrder', inplace = True) # Drop column chromosome order which is no longer required
    df2.to_csv(brookSumSorted, index=False) # Write the sorted dataframe to a CSV file
    globalend_time = time.perf_counter()
    print(f'\nThe summary is completed in {round(globalend_time-globalstart, 4)} second(s)\n')
