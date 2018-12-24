FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get install python-pip python-opencv python-qt4 -y
RUN pip2 install -U pip
RUN pip2 install numpy
RUN pip2 install PyMaxflow
RUN pip2 install opencv-python
