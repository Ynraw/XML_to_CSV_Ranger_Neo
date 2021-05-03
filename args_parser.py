import argparse
from argparse import ArgumentParser
from file_parser import FileParser
from csv_converter import CSVConverter
from xml_parser import XMLParser
import time

# Create parser
my_parser = argparse.ArgumentParser(prog='convert',
                                    usage='Convert and merge to CSV, all XML file output from PROMAX Ranger Explorer',
                                    description='Command Line Application that converts XML files to CSV')


# Add the arguments
my_parser.add_argument('path', type=str, help='the path to XML folder')
my_parser.add_argument('-ep', '--extract_params', action='store_true', help='include the transmit information to be extracted from the XML file.\nTransmit info might be absent if TS unlocked')
my_parser.add_argument('-m', '--merge', action='store_true', help='each XML files will be merged and converted to each CSV file')
my_parser.add_argument('-cat', '--categorize', action='store_true', help='files will be categorize as locked/unlocked Transport Stream')

# Excecute the arg_prse method
args = my_parser.parse_args()


def main():

    fp = FileParser(args.path)
    fp.create_folder()
    dir_path = fp.get_dir_path()
    file_name_list = fp.get_xml_files()
    file_gen = fp.generate_files()

    if not (args.categorize or args.merge or args.extract_params):
        for file in file_name_list:
            print(f'Converting {file} now....')
            xml_path = fp.get_file(file_gen)
            xml = XMLParser(xml_path)
            measurements = xml.measurements()
            csv = CSVConverter(dir_path, measurements)
            csv.promax_convert(file)
            print('\tSuccess...')

    elif args.categorize:
        print('categorize')

    elif args.merge:
        print('merge')

    elif args.extract_params:
        print('extracted')

if __name__ == '__main__':
    main()