
import argparse
from graph_cut import CutUIFolder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Interactive Graph Cut",
                                     description="Interactively segment an image", add_help=True)
    parser.add_argument('-i', '--INFILE', help='Input image file to segment.', required=True)

    args = parser.parse_args()

    ui = CutUIFolder.CutUIFolder(args.INFILE)
    ui.run()
