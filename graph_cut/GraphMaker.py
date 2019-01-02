
import cv2
import numpy as np
import maxflow
import os
from graph_cut import common
from graph_cut import Color


class GraphMaker:

    foreground = 1
    background = 0

    seeds = 0
    segmented = 1

    default = 0.5
    MAXIMUM = 1000000000

    def __init__(self):
        self.filename = None
        self.image = None
        self.graph = None
        self.overlay = None
        self.seed_overlay = None
        self.segment_overlay = None
        self.mask = None
        self.background_seeds = []
        self.foreground_seeds = []
        self.background_average = np.array(3)
        self.foreground_average = np.array(3)
        self.nodes = []
        self.edges = []
        self.current_overlay = self.seeds
        self.seed_point_size = 2
        self.erase_size = 3

    def load_image(self, filename):
        self.filename = filename
        self.image = cv2.imread(filename)
        self.graph = np.zeros_like(self.image)
        self.seed_overlay = np.zeros_like(self.image)
        self.segment_overlay = np.zeros_like(self.image)
        self.mask = None

    def resize_image(self, img, screen_width, screen_height):
        self.ori_width = img.shape[1]
        self.ori_height = img.shape[0]
        screen_resolution = float(screen_height) / float(screen_width)
        image_resolution = float(self.ori_height) / float(self.ori_width)

        if image_resolution >= screen_resolution:
            target_height = screen_height
            target_width = self.ori_width * screen_height / self.ori_height
            self.image = cv2.resize(img, (int(target_width), int(target_height)), interpolation=cv2.INTER_CUBIC)
        else:
            target_width = screen_width
            target_height = self.ori_height * screen_width / self.ori_width
            self.image = cv2.resize(img, (int(target_width), int(target_height)), interpolation=cv2.INTER_CUBIC)

        self.resize_width = self.image.shape[1]
        self.resize_height = self.image.shape[0]
        self.graph = np.zeros_like(self.image)
        self.seed_overlay = np.zeros_like(self.image)
        self.segment_overlay = np.zeros_like(self.image)
        self.mask = None


    def add_seed(self, x, y, type):
        if self.image is None:
            print 'Please load an image before adding seeds.'
        x = float(x) / float(self.resize_width)
        y = float(y) / float(self.resize_height)
        if type == self.background:
            if not self.background_seeds.__contains__((x, y)):
                self.background_seeds.append((x, y))
                x = int(x * self.resize_width)
                y = int(y * self.resize_height)
                cv2.rectangle(self.seed_overlay, (x-self.seed_point_size, y-self.seed_point_size), (x+self.seed_point_size, y+self.seed_point_size), Color.cv_color_string_map["red"], -1)
        elif type == self.foreground:
            if not self.foreground_seeds.__contains__((x, y)):
                self.foreground_seeds.append((x, y))
                x = int(x * self.resize_width)
                y = int(y * self.resize_height)
                cv2.rectangle(self.seed_overlay, (x-self.seed_point_size, y-self.seed_point_size), (x+self.seed_point_size, y+self.seed_point_size), Color.cv_color_string_map["blue"], -1)

    def add_seed_make(self, x, y, type):
        if self.image is None:
            print
            'Please load an image before adding seeds.'
        if type == self.background:
            if not self.background_seeds.__contains__((x, y)):
                self.background_seeds.append((x, y))
                cv2.rectangle(self.seed_overlay, (x - self.seed_point_size, y - self.seed_point_size),
                              (x + self.seed_point_size, y + self.seed_point_size),
                              Color.cv_color_string_map["red"], -1)
        elif type == self.foreground:
            if not self.foreground_seeds.__contains__((x, y)):
                self.foreground_seeds.append((x, y))
                cv2.rectangle(self.seed_overlay, (x - self.seed_point_size, y - self.seed_point_size),
                              (x + self.seed_point_size, y + self.seed_point_size),
                              Color.cv_color_string_map["blue"], -1)
#########################################################################################################
    def delete_seed(self, x, y, type):
        if self.image is None:
            print
            'Please load an image before adding seeds.'
        if type == self.background:
            for (back_x, back_y) in self.background_seeds:
                back_x_up = int(back_x * self.resize_width)
                back_y_up = int(back_y * self.resize_height)
                if back_x_up > x - self.erase_size and back_y_up > y - self.erase_size and back_x_up < x + self.erase_size and back_y_up < y + self.erase_size:
                    self.background_seeds.remove((back_x, back_y))
                    cv2.rectangle(self.seed_overlay, (x - self.erase_size, y - self.erase_size),
                                  (x + self.erase_size, y + self.erase_size),
                                  Color.cv_color_string_map["black"],
                                  -1)

        elif type == self.foreground:
            for (back_x, back_y) in self.foreground_seeds:
                back_x_up = int(back_x * self.resize_width)
                back_y_up = int(back_y * self.resize_height)
                if back_x_up > x - self.erase_size and back_y_up > y - self.erase_size and back_x_up < x + self.erase_size and back_y_up < y + self.erase_size:
                    self.foreground_seeds.remove((back_x, back_y))
                    cv2.rectangle(self.seed_overlay, (x - self.erase_size, y - self.erase_size),
                                  (x + self.erase_size, y + self.erase_size),
                                  Color.cv_color_string_map["black"],
                                  -1)
###############################################################################################################################
    def clear_seeds(self):
        self.background_seeds = []
        self.foreground_seeds = []
        self.seed_overlay = np.zeros_like(self.seed_overlay)

    def clear_foreground_seeds(self):
        self.foreground_seeds = []
        self.seed_overlay = np.zeros_like(self.seed_overlay)
        for seed in self.background_seeds:
            x = seed[0]
            y = seed[1]
            x = int(x * self.resize_width)
            y = int(y * self.resize_height)
            cv2.rectangle(self.seed_overlay, (x - self.seed_point_size, y - self.seed_point_size), (x + self.seed_point_size, y + self.seed_point_size), Color.cv_color_string_map['red'], -1)

    def clear_background_seeds(self):
        self.background_seeds = []
        self.seed_overlay = np.zeros_like(self.seed_overlay)
        for seed in self.foreground_seeds:
            x = seed[0]
            y = seed[1]
            x = int(x * self.resize_width)
            y = int(y * self.resize_height)
            cv2.rectangle(self.seed_overlay, (x - self.seed_point_size, y - self.seed_point_size), (x + self.seed_point_size, y + self.seed_point_size), Color.cv_color_string_map['blue'], -1)

#########################################################################################################################
    def overlay_seeds(self, foreground, background):
        self.background_seeds = []
        self.foreground_seeds = []
        self.background_seeds = background
        self.foreground_seeds = foreground
        self.seed_overlay = np.zeros_like(self.seed_overlay)
        for seed in self.background_seeds:
            x = seed[0]
            y = seed[1]
            x = int(x * self.resize_width)
            y = int(y * self.resize_height)
            cv2.rectangle(self.seed_overlay, (x - self.seed_point_size, y - self.seed_point_size),
                          (x + self.seed_point_size, y + self.seed_point_size), Color.cv_color_string_map["red"], -1)

        for seed in self.foreground_seeds:
            x = seed[0]
            y = seed[1]
            x = int(x * self.resize_width)
            y = int(y * self.resize_height)
            cv2.rectangle(self.seed_overlay, (x - self.seed_point_size, y - self.seed_point_size),
                          (x + self.seed_point_size, y + self.seed_point_size), Color.cv_color_string_map["blue"], -1)

##########################################################################################################################
    def get_overlay(self):
        if self.current_overlay == self.seeds:
            return self.seed_overlay
        else:
            return self.segment_overlay

    def get_image_with_overlay(self, overlayNumber):
        if overlayNumber == self.seeds:
            return cv2.addWeighted(self.image, 0.9, self.seed_overlay, 0.4, 0.1)
        else:
            return cv2.addWeighted(self.image, 0.9, self.segment_overlay, 0.4, 0.1)

    def create_graph(self):
        if len(self.background_seeds) == 0 or len(self.foreground_seeds) == 0:
            print "Please enter at least one foreground and background seed."
            return

        print "Making graph"
        print "Finding foreground and background averages"
        self.find_averages()

        print "Populating nodes and edges"
        self.populate_graph()

        print "Cutting graph"
        self.cut_graph()

    def find_averages(self):
        self.graph = np.zeros((self.image.shape[0], self.image.shape[1]))
        print self.graph.shape
        self.graph.fill(self.default)
        self.background_average = np.zeros(3)
        self.foreground_average = np.zeros(3)

        for coordinate in self.background_seeds:
            self.graph[(coordinate[1] - 1)%self.image.shape[0], (coordinate[0] - 1)%self.image.shape[1]] = 0
            #self.background_average += self.image[coordinate[1], coordinate[0]]

        #self.background_average /= len(self.background_seeds)

        for coordinate in self.foreground_seeds:
            self.graph[(coordinate[1] - 1)%self.image.shape[0], (coordinate[0] - 1)%self.image.shape[1]] = 1
            #self.foreground_average += self.image[coordinate[1], coordinate[0]]

        #self.foreground_average /= len(self.foreground_seeds)

    def populate_graph(self):
        self.nodes = []
        self.edges = []

        # make all s and t connections for the graph
        for (y, x), value in np.ndenumerate(self.graph):
            # this is a background pixel
            if value == 0.0:
                self.nodes.append((self.get_node_num(x, y, self.image.shape), self.MAXIMUM, 0))

            # this is a foreground node
            elif value == 1.0:
                self.nodes.append((self.get_node_num(x, y, self.image.shape), 0, self.MAXIMUM))

            else:
                '''d_f = np.power(self.image[y, x] - self.foreground_average, 2)
                d_b = np.power(self.image[y, x] - self.background_average, 2)
                d_f = np.sum(d_f)
                d_b = np.sum(d_b)
                e_f = d_f / (d_f + d_b)
                e_b = d_b / (d_f + d_b)'''
                self.nodes.append((self.get_node_num(x, y, self.image.shape), 0, 0))

                '''if e_f > e_b:
                    self.graph[y, x] = 1.0
                else:
                    self.graph[y, x] = 0.0'''

        for (y, x), value in np.ndenumerate(self.graph):
            if y == self.graph.shape[0] - 1 or x == self.graph.shape[1] - 1:
                continue
            my_index = self.get_node_num(x, y, self.image.shape)

            neighbor_index = self.get_node_num(x+1, y, self.image.shape)
            g = 1 / (1 + np.sum(np.power(self.image[y, x] - self.image[y, x+1], 2)))
            self.edges.append((my_index, neighbor_index, g))

            neighbor_index = self.get_node_num(x, y+1, self.image.shape)
            g = 1 / (1 + np.sum(np.power(self.image[y, x] - self.image[y+1, x], 2)))
            self.edges.append((my_index, neighbor_index, g))

    def cut_graph(self):
        self.segment_overlay = np.zeros_like(self.segment_overlay)
        self.mask = np.zeros_like(self.image, dtype=bool)
        g = maxflow.Graph[float](len(self.nodes), len(self.edges))
        nodelist = g.add_nodes(len(self.nodes))

        for node in self.nodes:
            g.add_tedge(nodelist[node[0]], node[1], node[2])

        for edge in self.edges:
            g.add_edge(edge[0], edge[1], edge[2], edge[2])

        flow = g.maxflow()

        for index in range(len(self.nodes)):
            if g.get_segment(index) == 1:
                xy = self.get_xy(index, self.image.shape)
                self.segment_overlay[xy[1], xy[0]] = (255, 0, 255)
                self.mask[xy[1], xy[0]] = (True, True, True)

    def swap_overlay(self, overlay_num):
        self.current_overlay = overlay_num

    def save_image(self, filename):
        if self.mask is None:
            print 'Please segment the image before saving.'
            return

        to_save = np.zeros_like(self.image)

        np.copyto(to_save, self.image, where=self.mask)
        cv2.imwrite(str(filename), to_save)

    def save_select_images(self, filename, b_masked_color = True, b_masked_gray = False, b_cut_color = False):
        if self.mask is None:
            print 'Please segment the image before saving.'
            return

        if b_masked_color is True:
            masked_color_image = self.get_image_with_overlay(self.segmented)
            fname, ext = os.path.splitext(filename)
            cv2.imwrite(str(fname) + '_masked_color' + str(ext), masked_color_image)

        if b_masked_gray is True:
            to_save = np.zeros([self.image.shape[0], self.image.shape[1]])
            white_img = np.zeros([self.image.shape[0], self.image.shape[1]])
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    white_img[x][y] = 255

            np.copyto(to_save, white_img, where=self.mask[:,:,0])
            cv2.imwrite(str(fname) + '_masked_gray' + str(ext), to_save)

        if b_cut_color is True:
            to_save = np.zeros_like(self.image)
            np.copyto(to_save, self.image, where=self.mask)
            cv2.imwrite(str(filename), to_save)


    def save_path_image(self, filename, outpath_masked_color, outpath_masked_gray, outpath_cut_color):
        if self.mask is None:
            print 'Please segment the image before saving.'
            return

        if outpath_masked_color is not None:
            fpath, fname, ext = common.split_path_filename_fileext(filename)
            masked_color_image = self.get_image_with_overlay(self.segmented)
            fpath = os.path.join(fpath, outpath_masked_color)
            fullpath = os.path.join(fpath, str(fname) + '.jpg')
            print('generate image : ' + fullpath)
            cv2.imwrite(fullpath, masked_color_image)

        if outpath_masked_gray is not None:
            fpath, fname, ext = common.split_path_filename_fileext(filename)
            fpath = os.path.join(fpath, outpath_masked_gray)
            fullpath = os.path.join(fpath, str(fname) + '.png')
            to_save = np.zeros([self.image.shape[0], self.image.shape[1]])
            white_img = np.zeros([self.image.shape[0], self.image.shape[1]])
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    white_img[x][y] = 255

            np.copyto(to_save, white_img, where=self.mask[:,:,0])
            print('generate image : ' + fullpath)
            cv2.imwrite(fullpath, to_save)

        if outpath_cut_color is not None:
            fpath, fname, ext = common.split_path_filename_fileext(filename)
            fpath = os.path.join(fpath, outpath_cut_color)
            fullpath = os.path.join(fpath, str(fname) + '.jpg')

            to_save = np.zeros_like(self.image)
            np.copyto(to_save, self.image, where=self.mask)
            print('generate image : ' + fullpath)
            cv2.imwrite(fullpath, to_save)

    def save_seeds(self):
        fpath, fname, ext = common.split_path_filename_fileext(self.filename)
        seed_folder = os.path.join(fpath, "seed")
        if os.path.isdir(seed_folder) == False:
            os.mkdir(seed_folder)

        fullpath = os.path.join(seed_folder, str(fname) + '_seed.txt')
        of = open(fullpath, 'w')

        of.writelines('foreground_seeds\n')
        for idx in self.foreground_seeds:
            idx = (int(idx[0]*self.ori_width), int(idx[1]*self.ori_height))
            of.writelines(str(idx) + '\n')

        of.writelines('background_seeds\n')
        for idx in self.background_seeds:
            idx = (int(idx[0]*self.ori_width), int(idx[1]*self.ori_height))
            of.writelines(str(idx) + '\n')
        of.close()



    def save_seeds_custom(self, fore, back, index):
        fpath, fname, ext = common.split_path_filename_fileext(self.filename)
        seed_folder = os.path.join(fpath, "seed")
        if os.path.isdir(seed_folder) == False:
            os.mkdir(seed_folder)

        fullpath = os.path.join(seed_folder, str(fname)+'-'+ fpath.split('/')[-1] + '-' + str(index) + '_seed.txt')
        of = open(fullpath, 'w')

        of.writelines('foreground_seeds\n')
        for idx in fore:
            idx = (int(idx[0]*self.ori_width), int(idx[1]*self.ori_height))
            of.writelines(str(idx) + '\n')

        of.writelines('background_seeds\n')
        for idx in back:
            idx = (int(idx[0]*self.ori_width), int(idx[1]*self.ori_height))
            of.writelines(str(idx) + '\n')
        of.close()


    def load_seeds(self, file):
        fpath, fname, ext = common.split_path_filename_fileext(self.filename)
        readfilename = os.path.join(fpath, "seed")
        readfilename = os.path.join(readfilename, file)
        readfile = open(readfilename, 'r')
        lines = readfile.readlines()

        read_mode = None
        self.background_seeds = []
        self.foreground_seeds = []

        for line in lines:
            line = line[:-1]
            if line == 'foreground_seeds':
                read_mode = self.foreground
                continue
            elif line == 'background_seeds':
                read_mode = self.background
                continue

            tuple_line = eval(line)

            if read_mode == self.foreground:
                self.add_seed_make(tuple_line[0], tuple_line[1], read_mode)
            elif read_mode == self.background:
                self.add_seed_make(tuple_line[0], tuple_line[1], read_mode)

        readfile.close()

    @staticmethod
    def get_node_num(x, y, array_shape):
        return y * array_shape[1] + x

    @staticmethod
    def get_xy(nodenum, array_shape):
        return (nodenum % array_shape[1]), (nodenum / array_shape[1])
