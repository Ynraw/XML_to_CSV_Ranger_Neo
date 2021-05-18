from lxml import etree as et
from random import *
import datetime
import os


def random_power():
    return round(random() + randint(15,60), 1), 'dBuV'

def random_latitude():
    return round(random(),7) + 10

def random_longitude():
    return round(random(),7) + 123

def random_altitude():
    return round(randrange(10,50))

def random_status_value():
    status = ['MPEG2 TS locked', 'No signal received']
    return choice(status)

def random_cn(power_value):
    cn = [None, 'dB']
    if power_value > 30 and power_value < 50:
        cn[0] = round(random() * 50, 1)
    if power_value < 30:
        cn[0] = round(random()) + randrange(0,10)
    if power_value >= 50:
        cn[0] = round(random()) + randrange(30,35)
    return cn

def random_mer(power_value):
    mer = [None, 'dB']
    if power_value < 30:
        mer[0] = randrange(10,20) + round(random(),1)
    elif power_value >= 30 and power_value < 45:
        mer[0] = randrange(20,30) + round(random(),1)
    elif power_value >= 45:
        mer[0] = randrange(30, 40) + round(random(),1)
    return mer

def random_cber(power_value):
    return random()/ 100000

def random_vber(power_value):
    return random()/ 100000

def random_lm(power_value):
    lm = [None, 'dB']
    if power_value < 30:
        lm[0] = randrange(-5,10)
    elif power_value >= 30 and power_value < 45:
        lm[0] = randrange(10,17)
    elif power_value >= 45:
        lm[0] = randrange(17, 25)
    return lm

def time_generator():
    h, m = 9, 0
    for num in range(0, 100000, 3):
        s = num % 60
        if num % 60 == 0 and num != 0:
            m += 1
        if m == 60:
            m = 0
            h += 1
        if h == 13:
            break
            s = 0
            m = 0
            h = 0
        time = datetime.time(h, m, s)
        yield time


def create_cpoint():

    root_child = ['INFORMATION'] + ['CPOINT'] * 2500
    info_child = ['DESCRIPTION', 'SETTINGS', 'CHANNEL']
    set_child = ['SAMPLING_TIME', 'TIME_SPAN']
    ch_child = ['MEASUREMENTS']
    measurements_child = ['ISBDT']
    isdbt_child = ['PARAMETERS'] + ['LAYER'] * 2
    param_child = ['BANDWIDTH','SPECTRALINVERSION', 'FFT_MODE', 'GUARD_INTERVAL']
    layer_child = ['PARAMETERS']
    parameters_child = ['CODERATE', 'CONSTELLATION', 'TIME_INTERLEAVING']
    parameters_child_values = ['3/4', '16QAM', '2']
    cpoint_child = ['GPS', 'STATUS', 'MEASURES']
    measures_child = ['POWER', 'CN', 'OFFSET', 'MER', 'CBER', 'VBER', 'LM']
    os_value = ('142.8', 'kHz')
    date = datetime.date(2021, 5, 30)
    time = time_generator()
    layer = ['A', 'B']
    
    root = et.Element('COVERAGE', trademark='xml_generator',
                              equipment='simulator',
                              id_='143',
                              sn='sn020492020',
                              band='rubber band',
                              version='.001',
                              mode='Coverage',
                              date='2020-09-16')

    for num,child in enumerate(root_child):
        if child != 'CPOINT':
            info = et.SubElement(root, child)
            for info_ch in info_child:
                if info_ch == 'DESCRIPTION':
                    desc = et.SubElement(info, info_ch)
                if info_ch == 'SETTINGS':
                    sett = et.SubElement(info, info_ch)
                    for set_c in set_child:
                        if set_c == 'SAMPLING_TIME':
                            sampl_time = et.SubElement(sett, set_c, value=' ', units=' ')
                        if set_c == 'TIME_SPAN':
                            time_span = et.SubElement(sett, set_c, value=' ', units=' ')
                if info_ch == 'CHANNEL':
                    chann = et.SubElement(info, info_ch, name="26", frequency="545.00", units="MHz", date="2020-09-16", time="02:59:27")
                    measur = et.SubElement(chann, 'MEASUREMENTS')
                    isdbt = et.SubElement(measur, 'ISDB-T')
                    for child in isdbt_child:
                        if child == 'PARAMETERS':
                            params = et.SubElement(isdbt, child)
                            for child in param_child:
                                if child == 'BANDWIDTH':
                                    bw = et.SubElement(params, child, value='6000', units='kHz')
                                if child == 'SPECTRALINVERSION':
                                    si = et.SubElement(params, child, value='OFF')
                                if child == 'FFT_MODE':
                                    fft = et.SubElement(params, child, value='8K')
                                if child == 'GUARD_INTERVAL':
                                    gi = et.SubElement(params, child, value='1/4')
                        if child == 'LAYER':
                            for lyr in layer:
                                if lyr == 'B': 
                                    layer = et.SubElement(isdbt, child, value=lyr)
                                    paramet = et.SubElement(layer, 'PARAMETERS', value=lyr)
                                    for param_child, val in zip(parameters_child, parameters_child_values):
                                        coderate = et.SubElement(paramet, param_child, value=val)
                                if lyr == 'A':
                                    layer = et.SubElement(isdbt, child, value=lyr)
        elif child == 'CPOINT':
            time_ = next(time)
            cpoint = et.SubElement(root, child, date=str(date), time=str(time_), id=str(num))
            for cpoint_ch in cpoint_child:
                if cpoint_ch == 'GPS':
                    lat = random_latitude()
                    long = random_longitude()
                    alt = random_altitude()
                    gps = et.SubElement(cpoint, cpoint_ch, latitude=str(lat), longitude=str(long), altitude=str(alt), locked='true')
                elif cpoint_ch == 'STATUS':
                    value = random_status_value()
                    status = et.SubElement(cpoint, cpoint_ch, value=value)
                elif cpoint_ch == 'MEASURES':
                    measures = et.SubElement(cpoint, cpoint_ch)
                    for m_child in measures_child:
                        if m_child == 'POWER':
                            power_value, units = random_power()
                            et.SubElement(measures, m_child, value=str(power_value), units=units)
                        if m_child == 'CN':
                            value, units = random_cn(power_value)
                            et.SubElement(measures, m_child, value=str(value), units=units)
                        if m_child == 'OFFSET':
                            value, units = '142.8', 'kHz'
                            et.SubElement(measures, m_child, value=value, units=units)
                        if m_child == 'MER':
                            value, units = random_mer(power_value)
                            et.SubElement(measures, m_child, value=str(value), units=units)
                        if m_child == 'CBER':
                            value = random_cber(power_value)
                            et.SubElement(measures, m_child, value=str(value))
                        if m_child == 'VBER':
                            value = random_vber(power_value)
                            et.SubElement(measures, m_child, value=str(value))
                        if m_child == 'LM':
                            value, units = random_lm(power_value)
                            et.SubElement(measures, m_child, value=str(value), units=units)
    return root


if __name__ == '__main__':

    if not os.path.exists('..\\test_xml'):
        os.mkdir('..\\test_xml')

    for num in range(1,11):
        root = create_cpoint()
        et.indent(root, space='    ')
        tree = et.ElementTree(root)
        fn = os.path.join('..\\test_xml', 'test')
        tree.write(fn + f'{num}.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")



