import os
import sys

class FileParser:

    def __init__(self, path):
        self._path = path
        self._number_of_files = len(self.get_xml_files())

    
    def get_xml_files(self):   
        """
        Returns a list of xml files.

        Fetch all xml files within a folder given a path to the 
        folder/directory.
        """
        try:
            files = [file for file in os.listdir(self._path) if file.endswith('.XML')]
        except:
            print('\n-------Missing directory. Might be a case of incorrect path/folder name. Please check.-------')
            sys.exit()

        if len(files) < 1:
            print('\n-------No XML files found, please check path directory or check folder-------')
            sys.exit()

        return files


    def create_folder(self):
        """Create CSV folder where csv files will be stored/saved."""
        if not os.path.exists(self._path + '/CSV'):
            os.mkdir(self._path + '/CSV')


    def get_file(self, file):
        """Returns a file including its file path.
        Accepts a filename and its path as the parameter.
        """
        return os.path.join(self._path, file)


    def get_number_of_files(self):
        return self._number_of_files