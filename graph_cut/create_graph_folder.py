
import argparse

import cv2
import numpy as np
from GraphMaker import GraphMaker

class CutCommand:

    def __init__(self, filename):
        self.graph_maker = GraphMaker()
        self.graph_maker.load_image(filename)

    def run(self):
        self.graph_maker.load_seeds("/home/jamin/Downloads/9003454992293_seed.txt")
        # self.graph_maker.save_seeds()
        # self.graph_maker.create_graph()
        # self.graph_maker.save_image("/home/jamin/Downloads/9003454992293_output.jpg")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Interactive Graph Cut",
                                     description="Interactively segment an image", add_help=True)
    parser.add_argument('-i', '--INFILE', help='Input image folder to segment.', required=True)

    args = parser.parse_args()

    cmd = CutCommand(args.INFILE)
    cmd.run()
