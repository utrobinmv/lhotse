import os
import sys

from .utils.tarindexer import indextar, lookup
from .utils import make_dirs
from . import constants

class TarReadClass:
    def __init__(self, tar_path: str, tar_filename: str):
        index_path = constants.TAR_PATH_INDEX
        meta_path = constants.TAR_PATH_META
        self.tar_path = tar_path
        self.tar_filename = tar_filename

        self.tar_fullname = os.path.join(tar_path, tar_filename)

        index_path = os.path.join(tar_path, index_path)
        make_dirs(index_path)

        meta_path = os.path.join(tar_path, meta_path)
        make_dirs(meta_path)
        
        self.tar_indexfilename = tar_filename.replace('.tar', '.index')
        self.dir_filename = tar_filename.replace('.tar', '.dir')

        self.tar_indexfilename = os.path.join(index_path, self.tar_indexfilename)
        self.dir_filename = os.path.join(meta_path, self.dir_filename)

        if not os.path.exists(self.tar_indexfilename):
            indextar(self.tar_fullname, self.tar_indexfilename)
            
        create_dir = False
        if not os.path.exists(self.dir_filename):
            create_dir = True
        
        self.dict_files = {}
        with open(self.tar_indexfilename, 'r') as outfile:
            if create_dir:
                dirfile = open(self.dir_filename, 'w')
            #self.filelist = []
            for line in outfile.readlines():
                m = line[:-1].rsplit(" ", 2)
                filename = m[0]
                size_i = int(m[2])
                #self.filelist.append(filename)
                self.dict_files[filename] = (int(m[1]), int(m[2]))
                if create_dir:
                    dirfile.write(filename + '\t' + str(size_i)+'\n')
                
            if create_dir:
                dirfile.close()

            
    def tarfs_ls(self):
        return list(self.dict_files.keys())
            
    def get_data_filename(self, filename: str):
        if filename not in self.dict_files.keys():
            assert False
        
        #def lookup(dbtarfile,indexfile,path):
        buffer = None
        with open(self.tar_fullname, 'rb') as tar:
            seek, size = self.dict_files[filename]
            tar.seek(seek)
            buffer = tar.read(size)
            #os.write (sys.stdout.fileno (), buffer)
        
        return buffer