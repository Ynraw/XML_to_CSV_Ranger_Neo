import pandas as pd

class CSVConverter:

    def __init__(self, dir_path, file_dict):
        self.path = dir_path
        #self.params = params
        self.file_dict = file_dict
        

    def get_df(self):
        return pd.DataFrame(self.file_dict)

    
    def promax_convert(self, file):
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

        return df.to_csv(self.path + file[:-4] + '.csv', index = False)

    def convert(self):
        df = self.get_df()

        return df.to_csv(self.path + file[:-4] + '.csv', index = False)

    def convert_with_params(self, file):
        df = self.get_df()
        for key in self.params.keys():
            df[key] = self.params[key]

        return df.to_csv(self.path + '/CSV/' + file[:-4] + '.csv', index = False)
    
    def concat(self):
        pass

    def categorize(self):
        df = self.get_df()
        MPEG_TS_locked = df.loc[df['STATUS']=='MPEG2 TS locked']
        No_Signal = df.loc[df['STATUS']=='No signal received']
        
        MPEG_TS_locked.to_csv(self.path + '/CSV/MPEG_TS_locked.csv', index = False)
        No_Signal.to_csv(self.path + '/CSV/No_Signal.csv', index = False)