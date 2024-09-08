import os

from .data_tar import TarReadClass

class LoadFileByFS:
    def __init__(self):
        self.tar_files = {}
    def load_fs_filename(self, root_dir:str, fullname: str):
        protocol = ''
        if fullname.startswith('tar://'):
            protocol = 'tar'
            list_tar_name = fullname.replace('tar://','').split('@')
            tar_name = list_tar_name[0]
            file_name = list_tar_name[1]
            data = self._load_tar_filename(root_dir, tar_name, file_name)
            return data
        else:
            assert False
    def load_fs_fullname(self, fullname: str):
        if fullname.find('@') > -1:
            tar_fullname, file_path = fullname.split('@')
            root_dir = os.path.dirname(tar_fullname)
            # base_name = os.path.basename(tar_fullname)
            load_name = fullname.replace(root_dir + '/', '')
            return self.load_fs_filename(root_dir, 'tar://' + load_name)
        else:
            assert False

    def _load_tar_filename(self, root_dir, tar_name, file_name):
        fullname = os.path.join(root_dir,tar_name)
        if fullname not in self.tar_files.keys():
            self.tar_files[fullname] = TarReadClass(root_dir, tar_name)

        data = self.tar_files[fullname].get_data_filename(file_name)
        return data
