import os
import sys
import zipfile
from .utils import make_dirs

from . import constants

class ZipReadClass:
    def __init__(self, zip_path: str, zip_filename: str):
        assert os.path.exists(zip_path)

        self.zip_path = zip_path
        self.zip_filename = zip_filename

        self.zip_fullname = os.path.join(zip_path, zip_filename)

        self.zip_ref = zipfile.ZipFile(self.zip_fullname, 'r')   

        self.list_files = self.zip_ref.namelist()     

        index_path = constants.TAR_PATH_INDEX
        meta_path = constants.TAR_PATH_META
        index_path = os.path.join(zip_path, index_path)
        # make_dirs(index_path)

        meta_path = os.path.join(zip_path, meta_path)
        make_dirs(meta_path)

        self.dir_filename = zip_filename.replace('.zip', '.dir')
        self.dir_filename = os.path.join(meta_path, self.dir_filename)

        # create dir
        if not os.path.exists(self.dir_filename):
            dirfile = open(self.dir_filename, 'w')
            for file_info in self.zip_ref.infolist():
                dirfile.write(file_info.filename + '\t' + str(file_info.file_size)+'\n')
            dirfile.close()

    def exists(self, filename: str):
        if filename not in self.list_files:
            return False
        return True

    def fslink_ls(self):
        return self.list_files
            
    def get_data_filename(self, filename: str):
        if filename not in self.list_files:
            assert False
        
        #def lookup(dbtarfile,indexfile,path):
        buffer = None
        with self.zip_ref.open(filename) as file:

            buffer = file.read()
            #os.write (sys.stdout.fileno (), buffer)
        
        return buffer