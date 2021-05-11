import pandas as pd

class CSVConverter:

    df_list = []

    def __init__(self, dir_path, file_dict):
        self.path = dir_path
        self.file_dict = file_dict

        

    # def __add__(self, *args, promax=True):
    #     if promax:
    #         p = [self.promax_convert()]
    #         for arg in args:
    #             p.append(arg.promax_convert())
    #         return pd.concat(p)
    #     else:
    #         p = [self.get_df()]
    #         for arg in args:
    #             p.append(arg.get_df())
    #         return pd.concat(p)


    def get_df(self):
        return pd.DataFrame(self.file_dict)

    
    def promax_convert(self):
        df = self.get_df()
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
        df.to_csv(self.path + file[:-4] + '.csv', index = False)
        print('\tSuccess...')
        return


    def convert_with_params(self, file):
        print(f'Converting {file} now....')
        df = self.get_df()
        df.to_csv(self.path + file[:-4] + '.csv', index = False)
        print('\tSuccess...')
        return


    def add_df_to_list(self, promax=True):
        if promax:
            CSVConverter.df_list.append(self.promax_convert())
        else:
            CSVConverter.df_list.append(self.get_df())


    def add_measurements_with_parameters_to_list(self):
        measurements_with_parameters = self.get_df()
        CSVConverter.df_list.append(measurements_with_parameters)


    def merge(self):
        print('Merging files...')
        df = pd.concat(self.df_list)
        return df

    
    def convert_merged(self, df):
        if df.shape[1] > 12:
            return df.to_csv(self.path + 'merge_with_parameters.csv', index = False)
        else:
            return df.to_csv(self.path + 'merge.csv', index = False)


    def categorize(self, df):
        print('Categorizing into MPEG2 TS status...')
        MPEG_TS_locked = df.loc[df['STATUS']=='MPEG2 TS locked']
        No_Signal = df.loc[df['STATUS']=='No signal received']
        
        MPEG_TS_locked.to_csv(self.path + 'MPEG_TS_locked.csv', index = False)
        No_Signal.to_csv(self.path + 'No_Signal.csv', index = False)