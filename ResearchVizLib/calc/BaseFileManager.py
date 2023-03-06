import os
import glob
import pandas
from pathlib import *
import numpy

class BaseFileManager:

    def containsPair(self, one_side :str, pool :list) -> bool:
        search_name: str
        one_side_path: Path = Path(one_side)
        if(one_side_path.stem.rsplit("_", 1)[-1] == "base"):
            search_name = os.path.join(str(one_side_path.parent), one_side_path.stem.rsplit("_", 1)[0] + one_side_path.suffix)
        else:
            search_name = os.path.join(str(one_side_path.parent), one_side_path.stem + "_base" + one_side_path.suffix)
        if(search_name in pool):
            return True
        else:
            return False

    def findPair(self, one_side :str, pool :list) -> str:
        search_name: str
        one_side_path: Path = Path(one_side)
        if(one_side_path.stem.rsplit("_", 1)[-1] == "base"):
            search_name = os.path.join(str(one_side_path.parent), one_side_path.stem.rsplit("_", 1)[0] + one_side_path.suffix)
        else:
            search_name = os.path.join(str(one_side_path.parent), one_side_path.stem + "_base" + one_side_path.suffix)
        if(self.containsPair(one_side, pool)):
            return search_name
        else:
            return "Error:such file does not exists at method:findPair"


    def isBaseFile(self, target_file :str):
        stem_name = Path(target_file).stem
        if(stem_name.rsplit("_", 1)[-1] == "base"):
            return True
        else:
            return False

    def extractBaseFiles(self, target_files :list):
        base_files = []
        for f in target_files:
            if(self.isBaseFile(f)):
                base_files.append(f)
        return base_files

    def createTrimmedCSV(self, box_dir, rows):
        content_files: list = glob.glob(box_dir + "\\*")
        file_names = []
        data_frames = []
        for f in content_files:
            if(os.path.isfile(f)):
                file_names.append(os.path.basename(f))
                with open(f, "r") as fp:
                    data_frames.append(self.extractRows(pandas.read_csv(fp), rows))
        new_dir = os.path.join(box_dir, os.path.splitext(os.path.basename(box_dir))[0] + "_trimmed")
        os.mkdir(new_dir)
        for i, file_name in enumerate(file_names):
            with open(os.path.join(new_dir, file_name), "w") as fp:
                data_frames[i].to_csv(fp, index=False)





base_rows = [0, 1, 9]
main_rows = [0, 5, 9]

dir_file = "C:\\Users\\genko\\Documents\\python_test"
file = "C:\\Users\\genko\\Documents\\python_test\\Φ=100nm.txt"
csv_manager = BaseFileManager()
# data_frame = csv_manager.convertToDataFrame(file)
# print(csv_manager.extractRows(data_frame,[0,5]))
#csv_manager.createTrimmedCSV(file, main_rows)
#print(csv_manager.isBaseFile(file))
inner_files = glob.glob(dir_file + "\\*")
print(inner_files)
print(csv_manager.containsPair(file, inner_files))
print(csv_manager.findPair(file, inner_files))
print(csv_manager.extractBaseFiles(inner_files))

