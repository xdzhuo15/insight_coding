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
    for key in small_dict: 
        if keystring in key.lower():
            return key

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

def ReadData( pathfile ):
    with open( pathfile, 'r' ) as csvfile:
        reader = csv.DictReader( csvfile, delimiter = ';' ) 
        # row1 is the first row
        row1 = next(reader)
        key_status = KeySearch_one( row1, 'STATUS' )
        key_occup = KeySearch_one( row1, 'SOC_NAME' )
        key_state = KeySearch_two( row1, 'WORK', 'STATE')        
        # initiate list values
        value_status = row1[key_status].lower()
        if value_status == 'certified':
            dat_occup = [ row1[key_occup] ]
            if (len(key_state) == 1):
                dat_state = [ row1[key_state[0]] ]
            else:
                # more than 1 keys, use the first valid value
                if ( row1[key_state[0]] == '' ):
                    dat_state = [ row1[key_state[1]] ]
                else:
                    dat_state = [ row1[key_state[0]] ]
        else:
            dat_state = []
            dat_occup = []            
        # append more certified values        
        for row in reader:
            value_status = row[key_status].lower()
            if value_status == 'certified':
                dat_occup.append( row[key_occup] )
                if ( len(key_state) == 1 ):
                    dat_state.append( row[key_state[0]] )
                else:
                    if (row[key_state[0]] == '' ):
                        dat_state.append( row[key_state[1]] )
                    else:    
                        dat_state.append( row[key_state[0]] )
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
        
