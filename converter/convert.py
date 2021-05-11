from argparse import ArgumentParser
from file_parser import FileParser
from csv_converter import CSVConverter
from xml_parser import XMLParser

# Create parser
my_parser = ArgumentParser(prog='convert_to_csv',
                           usage='Convert and merge to CSV, all XML file output from PROMAX Ranger Explorer',
                           description='Command Line Application that converts XML files to CSV',
                           )


# Add the arguments
my_parser.add_argument('path', type=str, help='the path to XML folder')
my_parser.add_argument('-ep', '--extract_params', action='store_true', help='include the transmit information to be extracted from the XML file.\
                                                                            \nTransmit info might be absent if TS unlocked')
my_parser.add_argument('-m', '--merge', action='store_true', help='each XML files will be merged first and converted to one CSV file')
my_parser.add_argument('-cat', '--categorize', action='store_true', help='files will be categorize as locked/unlocked Transport Stream')

# Excecute the arg_prse method
args = my_parser.parse_args()


def main():

    fp = FileParser(args.path)
    fp.create_folder()
    dir_path = fp.get_dir_path()
    csv_paths = fp.get_dir_paths()
    #path_name_list = fp.path_file_lists()
    file_name_list = fp.get_xml_files()
    file_gen = fp.generate_files()


    if args.extract_params:
        print('Preparing the files...')
        fn = [fp.get_file(file_gen) for _ in file_name_list]
        xml_obj = [XMLParser(path) for path in fn]                
        m = [xml.measurements_with_parameters() for xml in xml_obj]
        csvs = [CSVConverter(d, m) for d,m in zip(csv_paths, m)]
        if not args.merge:
            print('\nfiles prepared and ready to be converted...')
            [csv.convert_with_params(file) for csv,file in zip(csvs, file_name_list)]
        elif args.merge and args.categorize:
            print('\nfiles prepared and ready to be merge and categorize...')
            df_list = [csv.add_df_to_list(promax=False) for csv in csvs]
            merged_df = csvs[0].merge()
            csvs[0].categorize(merged_df)
        elif args.merge:
            print('\nfiles prepared and ready to be merge...')
            df_list = [csv.add_df_to_list(promax=False) for csv in csvs]
            merged_df = csvs[0].merge()
            csvs[0].convert_merged(merged_df)
 

    if not args.extract_params:
        print('Preparing the files....')
        fn = [fp.get_file(file_gen) for _ in file_name_list]
        xml_obj = [XMLParser(path) for path in fn]                
        m = [xml.measurements() for xml in xml_obj]              
        csvs = [CSVConverter(d, m) for d,m in zip(csv_paths, m)]
        if args.merge:
            print('\nfiles prepared and ready to be merge...')
            df_list = [csv.add_df_to_list(promax=True) for csv in csvs]
            merged_df = csvs[0].merge()
            csvs[0].convert_merged(merged_df)
        else:
            print('\nfiles prepared and ready to be converted...')
            [csv.convert(file) for csv,file in zip(csvs, file_name_list)]
            
    
if __name__ == '__main__':
    main()