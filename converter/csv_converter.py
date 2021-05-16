import pandas as pd
import os

class CSVConverter:

    df_list = []

    def __init__(self, dir_path, file_dict):
        self.path = dir_path
        self.file_dict = file_dict

  
    def promax_convert(self):
        df = pd.DataFrame(self.file_dict)
        df = df[['TEST POINT',
                 'DATE',
                 'TIME',
                 'LATITUDE',
                 'LONGITUDE',
                 'CH26 (MAIN) - POWER(dBuV)',
                 'CH26 (MAIN) - CN(dB)',
                 'CH26 (MAIN) - OFFSET(kHz)',
                 'CH26 (MAIN) - MER(dB)',
                 'CH26 (MAIN) - CBER',
                 'CH26 (MAIN) - VBER',
                 'CH26 (MAIN) - LM(dB)']]
        return df


    def convert(self, file):
        print(f'Converting {file} now....')
        df = self.promax_convert()
        csv_filename = os.path.join(self.path, file[:-4] + '.csv')
        df.to_csv(csv_filename, index = False)
        print('\tSuccess...')
        return


    def convert_with_params(self, file):
        print(f'Converting {file} now....')
        df = pd.DataFrame(self.file_dict)
        csv_filename = os.path.join(self.path, file[:-4] + '.csv')
        df.to_csv(csv_filename, index = False)
        print('\tSuccess...')
        return


    def add_df_to_list(self, promax=True):
        if promax:
            CSVConverter.df_list.append(self.promax_convert())
        else:
            CSVConverter.df_list.append(pd.DataFrame(self.file_dict))


    def merge(self):
        print('Merging files...')
        df = pd.concat(self.df_list)
        return df

    
    def convert_merged(self, df):
        if df.shape[1] > 12:
            csv_filename = os.path.join(self.path, 'merge_with_parameters.csv')
            return df.to_csv(csv_filename, index = False)
        else:
            csv_filename = os.path.join(self.path, 'merge.csv')
            return df.to_csv(csv_filename, index = False)


    def categorize(self, df):
        print('Categorizing into MPEG2 TS status...')
        MPEG_TS_locked = df.loc[df['STATUS']=='MPEG2 TS locked']
        No_Signal = df.loc[df['STATUS']=='No signal received']

        locked = os.path.join(self.path, 'MPEG_TS_locked.csv')
        no_signal = os.path.join(self.path, 'No_Signal.csv')

        MPEG_TS_locked.to_csv(locked, index = False)
        No_Signal.to_csv(no_signal, index = False)