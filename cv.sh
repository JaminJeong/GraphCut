#export PYTHONPATH="${PYTHONPATH}:$(HOME)/your/code/path"
export PYTHONPATH="${PYTHONPATH}:/home/jamin/projects/Code/GraphCut"

#python2 ./graph_cut/GraphCut.py -i "$(HOME)/your/image/path"
python2 ./graph_cut/GraphCut.py -i "/home/jamin/Downloads/test/waterMelon.jpg"
