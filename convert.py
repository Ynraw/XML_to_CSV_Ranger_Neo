# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:18:48 2021

@description: Created for XML files from PROMAX RANGER NEO Signal Coverage test to be converted to CSV file
                and separate out the no signal from the good and ready for uploading into QGIS.
@author: warny sembrano

"""

import os
import pandas as pd
from lxml import etree as et
import sys
import argparse
import time

# Create parser
my_parser = argparse.ArgumentParser(prog='convert',
                                    usage='Convert and merge to CSV, all XML file output from PROMAX Ranger Explorer',
                                    description='Command Line Application that converts XML files to CSV')

# Add the arguments
my_parser.add_argument('path', metavar='path', type=str, help='the path to XML folder')
my_parser.add_argument('-e', '--extract_all', action='store_true', help='include the transmit information to be extracted from the XML file')
my_parser.add_argument('-r', '--retain_file', action='store_true', help='do not merge the files')
my_parser.add_argument('-c', '--categorize', action='store_false', help='files are not categorize as locked/unlocked')


# Excecute the arg_prse method
args = my_parser.parse_args()


def get_folder(path_folder):
   
    """fetch all files within a folder give a path to the 
    folder/directory and returned as list"""
    
    try:
        folder = [file for file in os.listdir(path_folder) if file.endswith('.XML')]
    except:
        print('\n-------Missing directory. Might be a case of incorrect path/folder name. Please check.-------')
        sys.exit()

    if len(folder) < 1:
        print('\n-------No XML files, please check path directory or check folder-------')
        sys.exit()
        
    return folder

 
def separate_good(df):
    
    """seprate out drive test points that have Transport Stream locked signals 
    and those do not receive signal and returned as tuple of DataFrame"""
    
    return df.loc[df['STATUS']=='MPEG2 TS locked'],df.loc[df['STATUS']=='No signal received']


def get_file(file, path):
    
    """Returns a file including its file path.
    Accepts a filename and its path as the parameter"""
    
    return path + '/' + file


def dataframe(dic):
    
    """returns a pandas dataframe that accepts a dictionary as parameter"""
    
    df = pd.DataFrame(dic)
    return df


def concat(df_list):
    
    """Returns a concatenated dataframe and accepts a list of dataframe as parameter"""
    
    df = pd.concat(df_list)
    return df




def dictionary(cpoint_list):
    
    """Accepts a CPOINT list as parameter and 
    sift through it to extract the following (ID,DATE,ALTITUDE,LATITUDE,
    LONGITUDE,STATUS,POWER,CN,MER,CBER,VBER) save it to a dictionary called dic and returns the dictionary"""
    
    dic = {'TEST POINT':[],'DATE':[],
            'TIME':[],'ALTITUDE':[],'LATITUDE':[],
            'LONGITUDE':[],'STATUS':[],
            'CH26 (MAIN) - POWER(dBuV)':[],'CH26 (MAIN) - CN(dB)':[],
            'CH26 (MAIN) - OFFSET(kHz)':[],'CH26 (MAIN) - MER(dB)':[],
            'CH26 (MAIN) - CBER':[],'CH26 (MAIN) - VBER':[],'CH26 (MAIN) - LM(dB)':[]}
    
    for point in cpoint_list:
        try:
            dic['TEST POINT'].append(point.attrib['id'])
        except:
            dic['TEST POINT'].append(0)
        try:
            dic['DATE'].append(point.attrib['date'])
        except:
            dic['DATE'].append(0)
        try:
            dic['TIME'].append(point.attrib['time'])
        except:
            dic['TIME'].append(0)
        try:
            dic['ALTITUDE'].append(point.find('GPS').attrib['altitude'])
        except:
            dic['ALTITUDE'].append(0)
        try:
            dic['LATITUDE'].append(point.find('GPS').attrib['latitude'])
        except:
            dic['LATITUDE'].append(0)
        try:
            dic['LONGITUDE'].append(point.find('GPS').attrib['longitude'])
        except:
            dic['LONGITUDE'].append(0)
        try:
            dic['STATUS'].append(point.find('STATUS').attrib['value'])
        except:
            dic['STATUS'].append(0)
        try:
            dic['CH26 (MAIN) - POWER(dBuV)'].append(point.find('MEASURES').find('POWER').attrib['value'])
        except:
            dic['CH26 (MAIN) - POWER(dBuV)'].append(0)
        try:
            dic['CH26 (MAIN) - CN(dB)'].append(point.find('MEASURES').find('CN').attrib['value'])
        except:
            dic['CH26 (MAIN) - CN(dB)'].append(0)
        try:
            dic['CH26 (MAIN) - OFFSET(kHz)'].append(point.find('MEASURES').find('OFFSET').attrib['value'])
        except:
            dic['CH26 (MAIN) - OFFSET(kHz)'].append(0)
        try:
            dic['CH26 (MAIN) - MER(dB)'].append(point.find('MEASURES').find('MER').attrib['value'])
        except:
            dic['CH26 (MAIN) - MER(dB)'].append(0)
        try:
            dic['CH26 (MAIN) - CBER'].append(point.find('MEASURES').find('CBER').attrib['value'])
        except:
            dic['CH26 (MAIN) - CBER'].append(0)
        try:
            dic['CH26 (MAIN) - VBER'].append(point.find('MEASURES').find('VBER').attrib['value'])
        except:
            dic['CH26 (MAIN) - VBER'].append(0)
        try:
            dic['CH26 (MAIN) - LM(dB)'].append(point.find('MEASURES').find('LM').attrib['value'])
        except:
            dic['CH26 (MAIN) - LM(dB)'].append(0)
            
    return dic



def create_folder(path):
    
    """create CSV folder where csv files will be stored/saved"""
    
    if not os.path.exists(path + '/CSV'):
        os.mkdir(path + '/CSV') 


def get_path():

    if not os.path.isdir(args.path):
        print('\nThe path specified does not exist. type the command \'convert_v2 <folder path>\'')
        sys.exit()

    return args.path
    # try:                 
    #     path = sys.argv[1]
    # except:
    #     print("""\nPlease don\'t forget to type the target folder path
    #         type the command 'convert <folder path>'""")
    #     sys.exit()
    
    # return path


def main():

    converted_successfully = 0
    failed = 0
    df_list = []

    parser = et.XMLParser(ns_clean=True)
    path = get_path()
    files = get_folder(path)

        
    start_loop = time.time()
    for file in files:
        print(f'converting {file} file now...')
        xml = get_file(file, path)
        try:
            tree = et.parse(xml, parser)
        except:
            failed += 1
            print('Error detected...')
            print(f'\tPlease check <\COVERAGE> closing tag of {file}')
            continue
        
        root = tree.getroot()
        channel = root.find('INFORMATION').find('CHANNEL')
        isdbt = root.find('INFORMATION').find('CHANNEL').find('MEASUREMENTS').find('ISDB-T')
        cpoints = root.findall('CPOINT')
        cpoints_dictionary= dictionary(cpoints)
        df = dataframe(cpoints_dictionary)   
        print('\tsuccess...')
        df_list.append(df)
        converted_successfully += 1
       
    end_loop = time.time()

    output = concat(df_list)
    TS_locked, no_signal = separate_good(output)
    create_folder(path)

    TS_locked.to_csv(path + '/CSV/TS_locked.csv', index = False)
    no_signal.to_csv(path + '/CSV/no_signal.csv', index = False)

    print(f'\n{converted_successfully} file/s converted and merged successfully')
    print(f'{failed} file/s failed')
    print('Please check CSV folder.')
    print('loop_time: {}'.format(end_loop-start_loop))
    
    print(args)

if __name__ == '__main__':
    main()


























































