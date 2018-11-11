# Problem

Goals:
1) To create a mechanism to analyze past years data, specifically to calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

2) Code should be modular and reusable for future. 

3) By running the shell file run.sh, the data will be processed and results will be exported in txt files in folder ./output. 


# Input Dataset

Data needs to be put into the ./input folder in csv file: h1b_input.csv

# Code explanation

A review of the data shows the files in 2014-2016 have different headers for the columns in interest: status, occupation and work state. It is relatively easier to search for the first two, as the key words 'STATUS' and 'SOC_NAME' will differentiate the keys, regardless of the variations. However, work site is not that straight forward, and I use two key words 'WORK' and 'STATE' in a search that could return 1 or 2 results from the data for further processing.

2014 key words: 'STATUS', 'LCA_CASE_SOC_NAME', 'LCA_CASE_WORKLOC1_STATE','LCA_CASE_WORKLOC2_STATE'
2015 key words: 'CASE_STATUS', 'SOC_NAME', 'WORKSITE_STATE'
2016 key words: 'CASE_STATUS', 'SOC_NAME', 'WORKSITE_STATE'

Function ReadData reads in h1b_input.csv as dictionary, which is passed to functions KeySearch_one for selecting columns for status and occupation, and KeySearch_two for work site. Once we have the keys, we use the value of the status key to identify "certified" data, and compile the corresponding information for occupation and work state into two separate lists. I use Top10Sort to sort the list, calculate percentage and export in txt files. It sorts the data twice so that if two attributes has the same count of cases, the occupation or state will be sorted alphabetically.      
  
