import os
from pathlib import Path

from .data_tar import TarReadClass
from .data_zip import ZipReadClass

class LoadFileByFS:
    def __init__(self):
        self.tar_files = {}
        self.zip_files = {}
    def load_fs_filename(self, root_dir:str, fullname: str):
        protocol = ''
        if fullname.startswith('tar://'):
            protocol = 'tar'
            list_tar_name = fullname.replace('tar://','').split('@')
            tar_name = list_tar_name[0]
            file_name = list_tar_name[1]
            data = self._load_tar_filename(root_dir, tar_name, file_name)
            return data
        elif fullname.startswith('zip://'):
            protocol = 'zip'
            list_tar_name = fullname.replace('zip://','').split('@')
            tar_name = list_tar_name[0]
            file_name = list_tar_name[1]
            data = self._load_zip_filename(root_dir, tar_name, file_name)
            return data
        else:
            assert False


    def _load_file_link(self, tar_fullname: str):
        root_dir = os.path.dirname(tar_fullname)
        # base_name = os.path.basename(tar_fullname)
        load_name = tar_fullname.replace(root_dir + '/', '')

        extension = Path(tar_fullname).suffix
        if extension == '.tar':
            if tar_fullname not in self.tar_files.keys():
                file_link = TarReadClass(root_dir, load_name)
                self.tar_files[tar_fullname] = file_link
            else:
                file_link = self.tar_files[tar_fullname]
        elif extension == '.zip':
            if tar_fullname not in self.zip_files.keys():
                file_link = ZipReadClass(root_dir, load_name)
                self.zip_files[tar_fullname] = file_link
            else:
                file_link = self.zip_files[tar_fullname]
        else:
            assert False

        return file_link

    def listdir(self, tar_fullname: str):
        file_link = self._load_file_link(tar_fullname)
        return file_link.fslink_ls()

    def exists(self, tar_fullname: str):
        if tar_fullname.find('@') > -1:
            sp = tar_fullname.split('@')
            assert len(sp) == 2
            tar_filename = sp[0]
            find_filename = sp[1]
            file_link = self._load_file_link(tar_filename)
            return file_link.exists(find_filename)
        else:
            return False

    def load_fs_fullname(self, fullname: str):
        if fullname.find('@') > -1:
            tar_fullname, file_path = fullname.split('@')
            root_dir = os.path.dirname(tar_fullname)
            # base_name = os.path.basename(tar_fullname)
            load_name = fullname.replace(root_dir + '/', '')

            extension = Path(tar_fullname).suffix
            if extension == '.tar':
                return self.load_fs_filename(root_dir, 'tar://' + load_name)
            elif extension == '.zip':
                return self.load_fs_filename(root_dir, 'zip://' + load_name)
        else:
            assert False

    def _load_tar_filename(self, root_dir, tar_name, file_name):
        fullname = os.path.join(root_dir,tar_name)
        if fullname not in self.tar_files.keys():
            self.tar_files[fullname] = TarReadClass(root_dir, tar_name)

        data = self.tar_files[fullname].get_data_filename(file_name)
        return data

    def _load_zip_filename(self, root_dir, tar_name, file_name):
        fullname = os.path.join(root_dir,tar_name)
        if fullname not in self.zip_files.keys():
            self.zip_files[fullname] = ZipReadClass(root_dir, tar_name)

        data = self.zip_files[fullname].get_data_filename(file_name)
        return data
