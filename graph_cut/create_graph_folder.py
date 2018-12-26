
import argparse

import cv2
import numpy as np
import os
import glob

from GraphMaker import GraphMaker

class CutCommand:

    def __init__(self, filepath):
        self.graph_maker = GraphMaker()
        self.filepath = filepath

        self.folder_masked_color = os.path.join(self.filepath, "masked_color")
        self.folder_masked_gray = os.path.join(self.filepath, "masked_gray")
        self.folder_cut_color = os.path.join(self.filepath, "cut_color")

        if os.path.isdir(self.folder_masked_color) == False:
            print('make directory : ' + self.folder_masked_color)
            os.mkdir(self.folder_masked_color)
        if os.path.isdir(self.folder_masked_gray) == False:
            print('make directory : ' + self.folder_masked_gray)
            os.mkdir(self.folder_masked_gray)
        if os.path.isdir(self.folder_cut_color) == False:
            print('make directory : ' + self.folder_cut_color)
            os.mkdir(self.folder_cut_color)

        self.file_list = os.listdir(filepath)

    def run(self):
        for filename in self.file_list:
            fname, ext = os.path.splitext(filename)
            if ext == '.jpg':
                fullpath = os.path.join(self.filepath, filename)
                self.graph_maker.load_image(fullpath)
                for file in glob.glob(self.filepath+'/seed/'+filename.split('.')[0]+'*'):
                    self.graph_maker.load_seeds(file)
                    self.graph_maker.create_graph()
                    self.graph_maker.save_path_image(file.split('_seed')[0],
                                                     self.folder_masked_color,
                                                     self.folder_masked_gray,
                                                     self.folder_cut_color)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Interactive Graph Cut",
                                     description="Interactively segment an image", add_help=True)
    parser.add_argument('-i', '--INFILE', help='Input image folder to segment.', required=True)

    args = parser.parse_args()

    cmd = CutCommand(args.INFILE)
    cmd.run()
