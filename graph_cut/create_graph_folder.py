
import argparse

import cv2
import numpy as np
import os

from GraphMaker import GraphMaker

class CutCommand:

    def __init__(self, filepath):
        self.graph_maker = GraphMaker()
        self.file_list = os.listdir(filepath)

    def run(self):
        for filename in self.file_list:
            fname, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.graph_maker.load_image(filename)
                seed_file = None
                seed_file = str(fname) + "_seed.txt"
                if seed_file == None:
                    print("seed_file is None!!")
                else:
                    self.graph_maker.load_seeds()
                    self.graph_maker.create_graph()
                    self.graph_maker.save_image(str(fname) + "_output.jpg")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Interactive Graph Cut",
                                     description="Interactively segment an image", add_help=True)
    parser.add_argument('-i', '--INFILE', help='Input image folder to segment.', required=True)

    args = parser.parse_args()

    cmd = CutCommand(args.INFILE)
    cmd.run()
