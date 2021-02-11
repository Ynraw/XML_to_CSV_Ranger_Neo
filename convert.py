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
from sys import argv


def get_folder(path_folder):
    
    """fetch all files within a folder give a path to the 
    folder/directory and returned as list"""
    
    try:
        folder = [file for file in os.listdir(path_folder) if file.endswith('.XML')]
    except:
        print('\nInvalid folder path. Please check...')
        exit()
    return folder

    
def params(coverage):
    
    """extract the following parameters (CHANNEL, FREQUENCY,
    FFT_MODE, GUARD_INTERVAL, CODERATE, CONSTELLATION, TIME_INTERLEAVING)
    of the given drive test file from PROMAX NEO ranger
    and return all the parameters as tuple"""
    try:
        CHANNEL = root.find('INFORMATION').find('CHANNEL').attrib['name']
        FREQUENCY = root.find('INFORMATION').find('CHANNEL').attrib['frequency']
        FFT_MODE = root.find('INFORMATION').find('CHANNEL').find('MEASUREMENTS').find('ISDB-T').find('PARAMETERS').find('FFT_MODE').attrib['value']
        GUARD_INTERVAL = root.find('INFORMATION').find('CHANNEL').find('MEASUREMENTS').find('ISDB-T').find('PARAMETERS').find('GUARD_INTERVAL').attrib['value']
        CODERATE = root.find('INFORMATION').find('CHANNEL').find('MEASUREMENTS').find('ISDB-T').findall('LAYER')[1].find('PARAMETERS').find('CODERATE').attrib['value']
        CONSTELLATION = root.find('INFORMATION').find('CHANNEL').find('MEASUREMENTS').find('ISDB-T').findall('LAYER')[1].find('PARAMETERS').find('CONSTELLATION').attrib['value']
        TIME_INTERLEAVING = root.find('INFORMATION').find('CHANNEL').find('MEASUREMENTS').find('ISDB-T').findall('LAYER')[1].find('PARAMETERS').find('TIME_INTERLEAVING').attrib['value']
    except:
        CHANNEL, FREQUENCY, FFT_MODE, GUARD_INTERVAL, CODERATE, CONSTELLATION, TIME_INTERLEAVING = 0,0,0,0,0,0,0
    
    return CHANNEL, FREQUENCY, FFT_MODE, GUARD_INTERVAL, CODERATE, CONSTELLATION, TIME_INTERLEAVING


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
    
    succeed = True
    dic = {'ID':[],'DATE':[],
            'ALTITUDE':[],'LATITUDE':[],
            'LONGITUDE':[],'STATUS':[],
            'POWER':[],'CN':[],'MER':[],
            'CBER':[],'VBER':[]}
    
    for point in cpoint_list:
        try:
            dic['ID'].append(point.attrib['id'])
            dic['DATE'].append(point.attrib['date'])
            dic['ALTITUDE'].append(point.find('GPS').attrib['altitude'])
            dic['LATITUDE'].append(point.find('GPS').attrib['latitude'])
            dic['LONGITUDE'].append(point.find('GPS').attrib['longitude'])
            dic['STATUS'].append(point.find('STATUS').attrib['value'])      
            dic['POWER'].append(point.find('MEASURES').find('POWER').attrib['value'])
            dic['CN'].append(point.find('MEASURES').find('CN').attrib['value'])
            dic['MER'].append(point.find('MEASURES').find('MER').attrib['value'])    
            dic['CBER'].append(point.find('MEASURES').find('CBER').attrib['value'])
            dic['VBER'].append(point.find('MEASURES').find('VBER').attrib['value'])
        except:
            succeed = False
            
    return dic, succeed


def add_params(parameters, df):
    
    """add the following parameter values(CHANNEL, FREQUENCY,
    FFT_MODE, GUARD_INTERVAL, CODERATE, CONSTELLATION, TIME_INTERLEAVING) which is
    stored in the parameters tuple, to the dataframe values and return a completed dataframe"""
    
    param_list = ['CHANNEL','FREQUENCY',
                  'FFT_MODE','GUARD_INTERVAL',
                  'CODERATE','CONSTELLATION',
                  'TIME_INTERLEAVING']
    for param,val in zip(param_list,parameters):
        df[param] = val
        
    return df


def create_folder(path):
    
    """create CSV folder where csv files will be stored/saved"""
    
    if not os.path.exists(path + '/CSV'):
        os.mkdir(path + '/CSV') 
    

df_list = []
parser = et.XMLParser(ns_clean=True)
try:                 
    path = argv[1]
except:
    print("""\nPlease don\'t forget to type the target folder path
          type the command 'python convert <folder path>'""")
    exit()

files = get_folder(path)

converted_successfully = 0
failed = 0

if bool(files):
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
        params_ = params(root)
        cpoints = root.findall('CPOINT')
        cpoints_dictionary,succeed = dictionary(cpoints)
        if succeed:
            converted_successfully += 1
            df = dataframe(cpoints_dictionary)
            print('\tsuccess...')
        else:
            failed += 1
            print(f'Error detected in {file} file')
            print('\tfailed...')
            continue
        df_complete = add_params(params_, df)
        df_list.append(df_complete)
else:
    print('\n-------No XML files, please check path directory or check folder--------')
    exit()
    
output = concat(df_list)
good, no_signal = separate_good(output)
create_folder(path)

# please change the the path new folder name and filename
good.to_csv(path + '/CSV/good.csv', index = False)
no_signal.to_csv(path + '/CSV/no_signal.csv', index = False)

print(f'\n{converted_successfully} files converted successfully')
print(f'{failed} files failed')
print('Please check CSV folder.')


























































