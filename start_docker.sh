docker run -it --net=host --privileged -e DISPLAY --name 'graphcut_update' \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /etc/group:/etc/group:ro \
  -v /etc/passwd:/etc/passwd:ro \
  -v $HOME:$HOME \
  -w=$(pwd) \
  -u=$UID:$(id -g $USER) \
  -p 9999:8888 \
  -p 7007:6006 \
  --env QT_X11_NO_MITSHM=1 \
  mooneclipse03/graphcut \
  /bin/bash
