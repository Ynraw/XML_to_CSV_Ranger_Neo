import argparse
from argparse import ArgumentParser
from file_parser import FileParser
from csv_converter import CSVConverter
from xml_parser import XMLParser


# Create parser
my_parser = argparse.ArgumentParser(prog='convert',
                                    usage='Convert and merge to CSV, all XML file output from PROMAX Ranger Explorer',
                                    description='Command Line Application that converts XML files to CSV')


# Add the arguments
my_parser.add_argument('path', type=str, help='the path to XML folder')
my_parser.add_argument('-ep', '--extract_params', action='store_true', help='include the transmit information to be extracted from the XML file.\nTransmit info might be absent if TS unlocked')
my_parser.add_argument('-rf', '--retain_file', action='store_true', help='each XML files will be converted to each CSV file')
my_parser.add_argument('-cat', '--categorize', action='store_false', help='files are not categorize as locked/unlocked')
my_parser.add_argument('-pc', '--promax_convert', action='store_true', help='convert every file as CSV the same as Promax Website at https://www.promax.es/tools/kml-generator/')


# Excecute the arg_prse method
args = my_parser.parse_args()


def main():

    fp = FileParser(args.path)
    fp.create_folder()
    file_name_list = fp.get_xml_files()

    file_gen = fp.generate_files()

    for file in file_name_list:
        print(f'Converting {file} now....')
        xml_path = fp.get_file(file_gen)
        xml = XMLParser(xml_path)
        measurements = xml.measurements()
        csv = CSVConverter(args.path, measurements)
        csv.promax_convert(file)
        print('\tSuccess...')


if __name__ == '__main__':
    main()



    

