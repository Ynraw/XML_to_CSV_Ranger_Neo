from lxml import etree as et

class XMLParser:

    def __init__(self, xml):
        self.xml = xml
        self.dict_measures = {'TEST POINT':[],'DATE':[],'TIME':[],'ALTITUDE':[],
            'LATITUDE':[],'LONGITUDE':[],'STATUS':[],'CH26 (MAIN) - POWER(dBuV)':[],
            'CH26 (MAIN) - CN(dB)':[],'CH26 (MAIN) - OFFSET(kHz)':[],
            'CH26 (MAIN) - MER(dB)':[],'CH26 (MAIN) - CBER':[],'CH26 (MAIN) - VBER':[],
            'CH26 (MAIN) - LM(dB)':[]}
        self.dict_params = {'CHANNEL':None,'FREQUENCY':None,'FFT_MODE':None,'GUARD_INTERVAL':None,
                  'CODERATE':None,'CONSTELLATION':None,'TIME_INTERLEAVING':None}
        

    def get_parser(self):
        return et.XMLParser(ns_clean=True, recover=True)

    def get_tree(self):
        try:
            tree = et.parse(self.xml, self.get_parser())
        except:
            print('Error detected...')
            print(f'\tPlease check <\COVERAGE> closing tag of {file}')
            return None  
        return tree 


    def get_root(self):
        tree = self.get_tree()
        return tree.getroot()


    def get_cpoint_list(self):
        return self.get_root().findall('CPOINT')


    def get_channel(self):
        root = self.get_root()
        channel = root.find('INFORMATION').find('CHANNEL')
        return channel


    def get_isdbt(self):
        root = self.get_root()
        isdbt = root.find('INFORMATION').find('CHANNEL').find('MEASUREMENTS').find('ISDB-T')
        return isdbt

    
    def measurements(self):
   
        for point in self.get_cpoint_list():
            try:
                self.dict_measures['TEST POINT'].append(point.attrib['id'])
            except:
                self.dict_measures['TEST POINT'].append(0)
            try:
                self.dict_measures['DATE'].append(point.attrib['date'])
            except:
                self.dict_measures['DATE'].append(0)
            try:
                self.dict_measures['TIME'].append(point.attrib['time'])
            except:
                self.dict_measures['TIME'].append(0)
            try:
                self.dict_measures['ALTITUDE'].append(point.find('GPS').attrib['altitude'])
            except:
                self.dict_measures['ALTITUDE'].append(0)
            try:
                self.dict_measures['LATITUDE'].append(point.find('GPS').attrib['latitude'])
            except:
                self.dict_measures['LATITUDE'].append(0)
            try:
                self.dict_measures['LONGITUDE'].append(point.find('GPS').attrib['longitude'])
            except:
                self.dict_measures['LONGITUDE'].append(0)
            try:
                self.dict_measures['STATUS'].append(point.find('STATUS').attrib['value'])
            except:
                self.dict_measures['STATUS'].append(0)
            try:
                self.dict_measures['CH26 (MAIN) - POWER(dBuV)'].append(point.find('MEASURES').find('POWER').attrib['value'])
            except:
                self.dict_measures['CH26 (MAIN) - POWER(dBuV)'].append(0)
            try:
                self.dict_measures['CH26 (MAIN) - CN(dB)'].append(point.find('MEASURES').find('CN').attrib['value'])
            except:
                self.dict_measures['CH26 (MAIN) - CN(dB)'].append(0)
            try:
                self.dict_measures['CH26 (MAIN) - OFFSET(kHz)'].append(point.find('MEASURES').find('OFFSET').attrib['value'])
            except:
                self.dict_measures['CH26 (MAIN) - OFFSET(kHz)'].append(0)
            try:
                self.dict_measures['CH26 (MAIN) - MER(dB)'].append(point.find('MEASURES').find('MER').attrib['value'])
            except:
                self.dict_measures['CH26 (MAIN) - MER(dB)'].append(0)
            try:
                self.dict_measures['CH26 (MAIN) - CBER'].append(point.find('MEASURES').find('CBER').attrib['value'])
            except:
                self.dict_measures['CH26 (MAIN) - CBER'].append(0)
            try:
                self.dict_measures['CH26 (MAIN) - VBER'].append(point.find('MEASURES').find('VBER').attrib['value'])
            except:
                self.dict_measures['CH26 (MAIN) - VBER'].append(0)
            try:
                self.dict_measures['CH26 (MAIN) - LM(dB)'].append(point.find('MEASURES').find('LM').attrib['value'])
            except:
                self.dict_measures['CH26 (MAIN) - LM(dB)'].append(0)
    
        return self.dict_measures


    def parameters(self):
        """extract the following parameters (CHANNEL, FREQUENCY,
        FFT_MODE, GUARD_INTERVAL, CODERATE, CONSTELLATION, TIME_INTERLEAVING)
        of the given drive test file from PROMAX NEO ranger
        and return all the parameters as tuple
        """
        channel_ = self.get_channel()
        isdbt = self.get_isdbt()

        try:
            name = channel_.attrib['name']
            self.dict_params['CHANNEL'] = name
        except:
            self.dict_params['CHANNEL'] = 0
        try:
            self.dict_params['FREQUENCY'] = channel_.attrib['frequency']
        except:
            self.dict_params['FREQUENCY'] = 0
        try:
            self.dict_params['FFT_MODE'] = isdbt.find('PARAMETERS').find('FFT_MODE').attrib['value']
        except:
            self.dict_params['FFT_MODE'] = 0
        try:
            self.dict_params['GUARD_INTERVAL'] = isdbt.find('PARAMETERS').find('GUARD_INTERVAL').attrib['value']
        except:
            self.dict_params['GUARD_INTERVAL'] = 0
        try:
            if isdbt.findall('LAYER')[1].getchildren():
                self.dict_params['CODERATE'] = isdbt.findall('LAYER')[1].find('PARAMETERS').find('CODERATE').attrib['value']
            else:
                self.dict_params['CODERATE'] = isdbt.findall('LAYER')[0].find('PARAMETERS').find('CODERATE').attrib['value']
        except:
            self.dict_params['CODERATE'] = 0
        try:
            if isdbt.findall('LAYER')[1].getchildren():
                self.dict_params['CONSTELLATION'] = isdbt.findall('LAYER')[1].find('PARAMETERS').find('CONSTELLATION').attrib['value']
            else:
                self.dict_params['CONSTELLATION'] = isdbt.findall('LAYER')[0].find('PARAMETERS').find('CONSTELLATION').attrib['value']
        except:
            self.dict_params['CONSTELLATION'] = 0
        try:
            if isdbt.findall('LAYER')[1].getchildren():
                self.dict_params['TIME_INTERLEAVING'] = isdbt.findall('LAYER')[1].find('PARAMETERS').find('TIME_INTERLEAVING').attrib['value']
            else:
                self.dict_params['TIME_INTERLEAVING'] = isdbt.findall('LAYER')[0].find('PARAMETERS').find('TIME_INTERLEAVING').attrib['value']
        except:
            self.dict_params['TIME_INTERLEAVING'] = 0
        
        return self.dict_params

    
    def measurements_with_parameters(self):
        p = self.parameters()
        m = self.measurements()
        p.update(m)
        return p