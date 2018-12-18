#export PYTHONPATH="${PYTHONPATH}:$(HOME)/your/code/path"
export PYTHONPATH="${PYTHONPATH}:${pwd}"

#python2 ./graph_cut/GraphCutFolder.py -i "$(HOME)/your/image/foloer/path"
python2 ./graph_cut/GraphCutFolder.py -i "/home/jamin/Downloads/test"
