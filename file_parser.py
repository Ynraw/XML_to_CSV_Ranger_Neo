import os
import sys
import glob

class FileParser:

    def __init__(self, path):
        self._path = path
        self._number_of_files = len(self.get_xml_files())


    def get_xml_files(self):
        files = self.path_file_lists()
        filenames = [os.path.split(file)[-1] for file in files]        
        return sorted(filenames)


    def create_folder(self, name):
        """Create CSV folder where csv files will be stored/saved."""
        csv_folder = os.path.join(self._path, name)
        if not os.path.exists(csv_folder):
            os.mkdir(csv_folder)
        return csv_folder


    def get_dir_paths(self, csv_folder):
        total_files = len(self.path_file_lists())
        return [csv_folder for _ in range(total_files)]


    def path_file_lists(self):
        if not os.path.isdir(self._path):
            print('\n-------Missing directory. Might be a case of incorrect path/folder name. Please check.-------')
            sys.exit()
        else:
            files =  glob.glob(os.path.join(self._path, '*.XML'))
            if len(files) < 1:
                print('\n-------No XML files found, please check path directory or check folder-------')
                sys.exit()
        return sorted(files)