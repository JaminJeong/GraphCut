# GraphCut

An implementation of the graph cut algorithm with a custom GUI written in PyQt. 
Using the interface users mark the foreground and background of the image. Using this information,
the program builds a graph from the image pixels where the weights between pixels
represent the difference between them. To segment the image a minimum cut is performed on the graph.

The interface:
![GUI](https://github.com/mooneclipse03/GraphCut/blob/master/images/graphCut.png "Custom PyQT interface")

And an example result:

![before](https://github.com/mooneclipse03/GraphCut/blob/master/resource/dood.jpg "Before")
![after](https://github.com/mooneclipse03/GraphCut/blob/master/images/segmented.png "After")

## To run the program start up
### QT
```bash
sh QtGui.sh
```

### OpenCV UI
necessary, one input file and one output file
```bash
sh cv.sh
```

### OpenCV UI (sub-folders)
It split calculation and user's guide
#### draw user's guide
##### key event
 * s : previous image
 * d : next image
 * c : clear seed
 * f : clear foreground seed
 * b : clear background seed
 * t : change seed's mode (foreground mode or bach background mode)
 * ESC : exit

```bash
sh cvFolder.sh
```
#### calculation
```bash
sh create_graph_folder.sh
cd /your/image/file/path
tree -d
.
├── cut_color
├── masked_color
├── masked_gray
└── seed
```

## Requirements
* python2
* opencv >= 3.4
* numpy
* PyMaxflow
* PyQt4

## Reference


[1] [NathanZabriskie/GraphCut](https://github.com/NathanZabriskie/GraphCut) <br/>
