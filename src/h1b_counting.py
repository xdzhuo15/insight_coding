#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 22:00:19 2018

@author: xdzhuo
"""

import sys
import csv


def KeySearch_one( small_dict, keystring ):
    # search if there is only one key word
    keystring = keystring.lower() 
    keys = []
    for key in small_dict: 
        if keystring in key.lower():
            keys.append(key)
    return keys        

def KeySearch_two( small_dict, keystring1, keystring2 ):  
    # search with two key words 
    # if two results, return both results 
    keystring1 = keystring1.lower() 
    keystring2 = keystring2.lower() 
    keys = []        
    for key in small_dict:
        if keystring1 in key.lower() and keystring2 in key.lower():
            keys.append(key)
    return keys

def FindList( row, dat_select, key_select, key_criteria, set_criteria  ):
    # find recode according to criteria and append to list
    # row of dictionary, column selected, key of interest ( <= 1 ), and
    # key of criteria (status), and value of criteria
    value_criteria = row[key_criteria[0]].lower()
    n_key = len(key_select)
    i_key = n_key - 1
    if value_criteria == set_criteria:
        # go from the last key in key_select and use the first non-empty field
        while i_key >= 0:
            if ( row[key_select[i_key]] != '' or i_key == 0 ):
                break;
            else:
                i_key -= 1                                 
        dat_select.append( row[key_select[i_key]] ) 
    
def ReadData( pathfile ):
    with open( pathfile, 'r' ) as csvfile:
        reader = csv.DictReader( csvfile, delimiter = ';' ) 
        # row1 is the first row
        row1 = next(reader)
        key_status = KeySearch_one( row1, 'STATUS' )
        key_occup = KeySearch_one( row1, 'SOC_NAME' )
        key_state = KeySearch_two( row1, 'WORK', 'STATE') 
        value_status = 'certified'
        # initiate list values
        dat_state = []
        dat_occup = [] 
        # first row
        FindList( row1, dat_state, key_state, key_status, value_status  )
        FindList( row1, dat_occup, key_occup, key_status, value_status  )
        #remaining rows               
        for row in reader:
            FindList( row, dat_state, key_state, key_status, value_status  )
            FindList( row, dat_occup, key_occup, key_status, value_status  )
    csvfile.close()
    return dat_occup, dat_state           

def Top10Sort( data, pathfile, header ):
    total_count = len( data )
    unique_value = list(set( data ))
    out_dat = []
    for value in unique_value:
        n_count = data.count( value )
        out_dat.append( [ value, n_count] )
    # sort data first alphabetically and then based on counts
    out_dat = sorted( out_dat, key=lambda item: item[0])
    out_dat = sorted( out_dat, reverse=True, key=lambda item: item[1])
    with open( pathfile, 'w' ) as f:
        f.write( header[0] + ";" + header[1] + ";" + header[2] + "\n" )
        # if the data has less or equal than 10 unique values, list all
        n_unique = len(unique_value)
        if n_unique > 10:
            range_value = 10
        else:
            range_value = n_unique    
        n_write = 0 
        i_write = 0
        while ( n_write < range_value and i_write < n_unique ):
            # remove none types in the count
            if (out_dat[i_write][0] != ''):
                n_count = out_dat[i_write][1]
                pct_count = float(n_count)/float(total_count)
                f.write( out_dat[i_write][0] + ";" + str(n_count) + ";" 
                         + "{:.1%}".format(pct_count) + "\n" )
                n_write += 1
            i_write += 1    
    f.close()
              
    
def main():
    if len(sys.argv) == 4:
        infile = sys.argv[1]
        outfile_occup = sys.argv[2]
        outfile_state = sys.argv[3]
    else:
        print( ' Error: double check the input and output directories.\n ' )
        infile = []
        
    if len(infile) > 0:
        dat_occup, dat_state = ReadData( infile )         
        header_occup = ['TOP_OCUUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 
                       'PERCENTAGE']
        header_state = ['TOP_STATS', 'NUMBER_CERTIFIED_APPLICATIONS', 
                       'PERCENTAGE']                           
        Top10Sort( dat_occup, outfile_occup, header_occup )
        Top10Sort( dat_state, outfile_state, header_state )   
        print( ' Data successfully processed! \n' )        
        
                
if __name__ == "__main__":
    main()         
        
