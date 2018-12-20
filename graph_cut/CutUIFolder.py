
import cv2
import os
import numpy as np
from GraphMaker import GraphMaker
from graph_cut import DrawText


class CutUIFolder:

    def __init__(self, foldername):
        self.graph_maker = GraphMaker()
        self.window = "Graph Cut"
        self.output_text = "Graph Cut"
        self.mode = self.graph_maker.foreground
        self.started_click = False
        self.file_list = os.listdir(foldername)
        self.foldername = foldername
        self.index = 0
        self.file_list_image = []

        if len(self.file_list) != 0:
            for idx, filename in enumerate(self.file_list):
                if filename.find('.jpg') != -1:
                    self.file_list_image.append(filename)
            self.file_list = []

            for idx, filename in enumerate(self.file_list_image):
                self.file_list.append(os.path.join(self.foldername, self.file_list_image[idx]))

            self.graph_maker.load_image(self.file_list[self.index])
            self.display_image = np.array(self.graph_maker.image)
            self.output_text = str("Graph Cut - [ ") + str(self.index + 1) + ' / ' + str(len(self.file_list)) + " ] " + self.file_list_image[self.index]

    def _refresh(self):
        self.graph_maker.clear_seeds()
        self.graph_maker.load_image(self.file_list[self.index])
        self.display_image = np.array(self.graph_maker.image)
        self.mode = self.graph_maker.foreground
        self.output_text = str("Graph Cut - [ ") + str(self.index + 1) + ' / ' + str(len(self.file_list)) + " ] " + self.file_list_image[self.index]

    def run(self):
        cv2.namedWindow(self.window)
        cv2.setMouseCallback(self.window, self.draw_line)

        while 1:
            display = cv2.addWeighted(self.display_image, 0.9, self.graph_maker.get_overlay(), 0.4, 0.1)
            text_background = np.zeros((50, display.shape[1], 3), np.uint8)
            text_background[:] = DrawText.Color.color_string_map['white']
            display_window = cv2.vconcat((display.copy(), text_background))
            DrawText.draw_FiilText(display_window, self.output_text, 10, int(display_window.shape[0]))
            cv2.imshow(self.window, display_window)
            key = cv2.waitKey(20) & 0xFF
            if key == 27:
                self.graph_maker.save_seeds()
                break
            elif key == ord('c'):
                self.graph_maker.clear_seeds()
            elif key == ord('f'):
                self.graph_maker.clear_foreground_seeds()
            elif key == ord('b'):
                self.graph_maker.clear_background_seeds()

            elif key == ord('s'): # previous
                self.graph_maker.save_seeds()
                if self.index > 0:
                    self.index -= 1
                    self._refresh()

            elif key == ord('d'): # next
                self.graph_maker.save_seeds()
                if self.index < len(self.file_list) - 1:
                    self.index += 1
                    self._refresh()

            elif key == ord('t'):
                self.mode = 1 - self.mode
                self.graph_maker.swap_overlay(self.graph_maker.seeds)

        cv2.destroyAllWindows()

    def draw_line(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.started_click = True
            self.graph_maker.add_seed(x - 1, y - 1, self.mode)

        elif event == cv2.EVENT_LBUTTONUP:
            self.started_click = False

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.started_click:
                self.graph_maker.add_seed(x - 1, y - 1, self.mode)
