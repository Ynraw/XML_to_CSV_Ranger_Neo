from pandas import DataFrame, concat


# class Converter(DataFrame):

#     def __init__(self, xml):
#         self._xml = xml
#         self._list_df = []
        

def separate_good(df):
    """Seprate out drive test points that have Transport Stream locked signals 
    and those do not receive signal and returned as tuple of DataFrame.
    """
    return df.loc[df['STATUS']=='MPEG2 TS locked'],df.loc[df['STATUS']=='No signal received']


def dataframe(dic):
    """Returns a pandas dataframe that accepts a dictionary as parameter."""
    df = DataFrame(dic)
    return df


def concat_(df_list):
    """Returns a concatenated dataframe and accepts a list of dataframe as parameter."""
    df = concat(df_list)
    return df


def add_params(parameters, df):    
    """add the following parameter values(CHANNEL, FREQUENCY,
    FFT_MODE, GUARD_INTERVAL, CODERATE, CONSTELLATION, TIME_INTERLEAVING) which is
    stored in the parameters tuple, to the dataframe values and return a completed dataframe
    """
    param_list = ['CHANNEL','FREQUENCY',
                  'FFT_MODE','GUARD_INTERVAL',
                  'CODERATE','CONSTELLATION',
                  'TIME_INTERLEAVING']
    for param,val in zip(param_list,parameters):
        df[param] = val
        
    return df


def retain_file(df, path, file):
    #path = args.path
    df.to_csv(path + '/CSV/' + file[:-4] + '.csv', index = False)
    

def categorize(df, path):
    #path = args.path
    TS_locked, no_signal = separate_good(df)
    TS_locked.to_csv(path + '/CSV/TS_locked.csv', index = False)
    no_signal.to_csv(path + '/CSV/no_signal.csv', index = False)
    

# def convert_xml(file, fp):
#     parser = et.XMLParser(ns_clean=True, recover=True)
       
#     print(f'converting {file} file now...')
#     xml = fp.get_file(file)
#     try:
#         tree = et.parse(xml, parser)
#     except:
#         print('Error detected...')
#         print(f'\tPlease check <\COVERAGE> closing tag of {file}')
#         return 1
    
#     root = tree.getroot()
#     cpoints = root.findall('CPOINT')
#     cpoints_dictionary= dictionary(cpoints)
#     df = dataframe(cpoints_dictionary)   
#     print('\tsuccess...')
#     return df