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

# Excecute the parse_args method
args = my_parser.parse_args()


def main():
    
    fp = FileParser(args.path)  
    file_name_list = fp.get_xml_files()

    if args.extract_params:
        print('Preparing the files...')
        fn = fp.path_file_lists()
        xml_obj = [XMLParser(path) for path in fn]                
        m = [xml.measurements_with_parameters() for xml in xml_obj]
        if not args.merge:
            print('\nfiles prepared and ready to be converted...')
            csv_folder = fp.create_folder('csv_files_with_parameters')
            csv_paths = fp.get_dir_paths(csv_folder)
            csvs = [CSVConverter(d, m) for d,m in zip(csv_paths, m)]
            [csv.convert_with_params(file) for csv,file in zip(csvs, file_name_list)]
        elif args.merge and args.categorize:
            csv_folder = fp.create_folder('csv_merged_categorized')
            csv_paths = fp.get_dir_paths(csv_folder)
            print('\nfiles prepared and ready to be merge and categorize...')
            csvs = [CSVConverter(d, m) for d,m in zip(csv_paths, m)]
            [csv.add_df_to_list(promax=False) for csv in csvs]
            merged_df = csvs[0].merge()
            csvs[0].categorize(merged_df)
        elif args.merge:
            csv_folder = fp.create_folder('csv_merged')
            csv_paths = fp.get_dir_paths(csv_folder)
            print('\nfiles prepared and ready to be merge...')
            csvs = [CSVConverter(d, m) for d,m in zip(csv_paths, m)]
            [csv.add_df_to_list(promax=False) for csv in csvs]
            merged_df = csvs[0].merge()
            csvs[0].convert_merged(merged_df)
 

    if not args.extract_params:
        print('Preparing the files....')
        fn = fp.path_file_lists()
        xml_obj = [XMLParser(path) for path in fn]                
        m_dict = [xml.measurements() for xml in xml_obj]              
        
        if args.merge:
            csv_folder = fp.create_folder('csv_merged')
            csv_paths = fp.get_dir_paths(csv_folder)
            csvs = [CSVConverter(d, m) for d,m in zip(csv_paths, m_dict)]
            print('\nfiles prepared and ready to be merge...')
            [csv.add_df_to_list(promax=True) for csv in csvs]
            merged_df = csvs[0].merge()
            csvs[0].convert_merged(merged_df)
        else:
            csv_folder = fp.create_folder('csv_files')
            csv_paths = fp.get_dir_paths(csv_folder)
            csvs = [CSVConverter(d, m) for d,m in zip(csv_paths, m_dict)]
            print('\nfiles prepared and ready to be converted...')
            [csv.convert(file) for csv,file in zip(csvs, file_name_list)]
            
    
if __name__ == '__main__':
    main()
    print('Done')