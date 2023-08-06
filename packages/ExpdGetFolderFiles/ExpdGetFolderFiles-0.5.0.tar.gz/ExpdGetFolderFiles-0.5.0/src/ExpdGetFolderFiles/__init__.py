from os import path, walk
from loguru import logger


class GetFileList:
    def __init__(self, path, exts):
        self.file_path = path
        self.file_exts = exts.split(",")

    @property
    def files(self):
        file_list = []
        for root, dirs, files in walk(self.file_path):
            for ext in self.file_exts:
                [file_list.append(path.join(root, name)) for name in files if str(name).lower().endswith("."+ext.lower())]
        logger.debug(f"files totals: {len(file_list)}")
        return file_list


if __name__ == "__main__":
    files = GetFileList(path=r"C:\temp", exts="Html").files
    print(files)
