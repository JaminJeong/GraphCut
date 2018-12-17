docker run -it --net=host --privileged -e DISPLAY --name 'python2-opencv' \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /etc/group:/etc/group:ro \
  -v /etc/passwd:/etc/passwd:ro \
  -v $HOME:$HOME \
  -w=$(pwd) \
  -u=$UID:$(id -g $USER) \
  -p 9999:8888 \
  -p 7007:6006 \
  continuumai/car_recognition \ 
  /bin/bash
