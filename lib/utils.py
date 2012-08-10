import glob
import os

def getFileListByMask(directory, masks):
    file_list = []
    for mask in masks:
        file_list.extend(glob.glob(os.path.join(directory, mask)))
        file_list.extend(glob.glob(os.path.join(directory, mask.upper())))
    return file_list


class objDict(dict):
    def __getattribute__(self, key):
        if key in self:
            return self[key]