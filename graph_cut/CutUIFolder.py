
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
        self.obj_idx = 0
        self.file_list_image = []
        self.fixed_widht = 600

        if self.mode == 1:
            self.mode_name = 'foreground'
        else:
            self.mode_name = 'background'

        if len(self.file_list) != 0:
            for idx, filename in enumerate(self.file_list):
                if filename.find('.jpg') != -1:
                    self.file_list_image.append(filename)
            self.file_list = []

            for idx, filename in enumerate(self.file_list_image):
                self.file_list.append(os.path.join(self.foldername, self.file_list_image[idx]))

            self.graph_maker.load_image(self.file_list[self.index])
            self.graph_maker.resize_image(self.graph_maker.image, self.fixed_widht)
            self.display_image = np.array(self.graph_maker.image)
            self.output_text = self.mode_name + str("[ ") + str(self.index + 1) + ' / ' + str(
                    len(self.file_list)) + " ]" + self.file_list_image[self.index] + "[" + str(self.obj_idx) + "]"

        self.all_foreground_seed = [[]]*len(self.file_list_image)
        self.all_background_seed = [[]]*len(self.file_list_image)

        self.one_image_foreground_seed = []
        self.one_image_background_seed = []
    def _refresh(self):
        self.obj_idx = 0
        self.one_image_foreground_seed = self.all_foreground_seed[self.index][:]
        self.one_image_background_seed = self.all_background_seed[self.index][:]
        self.graph_maker.clear_seeds()
        self.graph_maker.load_image(self.file_list[self.index])
        self.graph_maker.resize_image(self.graph_maker.image, self.fixed_widht)

        try:
            self.graph_maker.overlay_seeds(foreground=self.one_image_foreground_seed[self.obj_idx][:],
                                       background=self.one_image_background_seed[self.obj_idx][:])
        except:
            self.graph_maker.overlay_seeds(foreground=self.one_image_foreground_seed[:],
                                           background=self.one_image_background_seed[:])
        self.display_image = np.array(self.graph_maker.image)
        self.mode = self.graph_maker.foreground
        if self.mode == 1:
            self.mode_name = 'foreground'
        else:
            self.mode_name = 'background'
        self.output_text = self.mode_name + str("[ ") + str(self.index + 1) + ' / ' + str(
                    len(self.file_list)) + " ]" + self.file_list_image[self.index] + "[" + str(self.obj_idx) + "]"
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
                try:
                    self.one_image_foreground_seed[self.obj_idx]
                except:
                    self.one_image_foreground_seed.append(self.graph_maker.foreground_seeds)
                    self.one_image_background_seed.append(self.graph_maker.background_seeds)
                else:
                    self.one_image_foreground_seed[self.obj_idx] = self.graph_maker.foreground_seeds
                    self.one_image_background_seed[self.obj_idx] = self.graph_maker.background_seeds
                for i in range(len(self.one_image_foreground_seed)):
                    self.graph_maker.save_seeds_custom(self.one_image_foreground_seed[i], self.one_image_background_seed[i], i)
                print("Complete save seed at this image")
            elif key == ord('c'):
                self.graph_maker.clear_seeds()
            elif key == ord('f'):
                self.graph_maker.clear_foreground_seeds()
            elif key == ord('b'):
                self.graph_maker.clear_background_seeds()

            elif key == ord('s'): # previous
                if self.index > 0:
                    self.one_image_save_seed()
                    self.all_foreground_seed[self.index] = self.one_image_foreground_seed
                    self.all_background_seed[self.index] = self.one_image_background_seed
                    self.index -= 1
                    self._refresh()


            elif key == ord('d'): # next
                if self.index < len(self.file_list)-1:
                    self.one_image_save_seed()
                    self.all_foreground_seed[self.index] = self.one_image_foreground_seed
                    self.all_background_seed[self.index] = self.one_image_background_seed
                    self.index += 1
                    self._refresh()

            elif key == ord('t'):
                self.mode = 1 - self.mode
                if self.mode == 1:
                    self.mode_name = 'foreground'
                else:
                    self.mode_name = 'background'

                self.output_text = self.mode_name + str("[ ") + str(self.index + 1) + ' / ' + str(
                    len(self.file_list)) + " ]" + self.file_list_image[self.index] + "[" + str(self.obj_idx) + "]"

                self.graph_maker.swap_overlay(self.graph_maker.seeds)

            elif key == ord('o'):
                if self.obj_idx >= 0:
                    self.one_image_save_seed()
                    self.graph_maker.clear_seeds()
                    if self.obj_idx > 0:
                        self.obj_idx -= 1
                    self.graph_maker.overlay_seeds(foreground=self.one_image_foreground_seed[self.obj_idx],
                                                   background=self.one_image_background_seed[self.obj_idx])
                    self.output_text = self.mode_name + str("[ ") + str(self.index + 1) + ' / ' + str(
                        len(self.file_list)) + " ]" + self.file_list_image[self.index] + "[" + str(self.obj_idx) +"]"


            elif key == ord('p'):
                self.one_image_save_seed()
                self.graph_maker.clear_seeds()
                self.obj_idx += 1
                try: self.one_image_foreground_seed[self.obj_idx]
                except:
                    print("Do Not Overlay")
                else:
                    self.graph_maker.overlay_seeds(foreground=self.one_image_foreground_seed[self.obj_idx],
                                                   background=self.one_image_background_seed[self.obj_idx])

                self.output_text = self.mode_name + str("[ ") + str(self.index + 1) + ' / ' + str(
                    len(self.file_list)) + " ]" + self.file_list_image[self.index] + "[" + str(self.obj_idx) +"]"

            elif key == ord('r'):
                if self.obj_idx > 0:
                    try:
                        self.one_image_foreground_seed[self.obj_idx]
                    except:
                        self.obj_idx -= 1
                        self.graph_maker.clear_seeds()
                        self.graph_maker.overlay_seeds(foreground=self.one_image_foreground_seed[self.obj_idx],
                                                       background=self.one_image_background_seed[self.obj_idx])
                        self.output_text = self.mode_name + str("[ ") + str(self.index + 1) + ' / ' + str(
                            len(self.file_list)) + " ]" + self.file_list_image[self.index] + "[" + str(
                            self.obj_idx) + "]"
                    else:
                        del self.one_image_foreground_seed[self.obj_idx]
                        del self.one_image_background_seed[self.obj_idx]
                        self.obj_idx -= 1
                        self.graph_maker.clear_seeds()
                        self.graph_maker.overlay_seeds(foreground=self.one_image_foreground_seed[self.obj_idx],
                                                       background=self.one_image_background_seed[self.obj_idx])
                        self.output_text = self.mode_name + str("[ ") + str(self.index + 1) + ' / ' + str(
                            len(self.file_list)) + " ]" + self.file_list_image[self.index] + "[" + str(self.obj_idx) + "]"

        cv2.destroyAllWindows()

    def draw_line(self, event, x, y, flags, param):

        if flags == cv2.EVENT_FLAG_CTRLKEY+cv2.EVENT_FLAG_LBUTTON:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.started_click = True
                self.graph_maker.delete_seed(x - 1, y - 1, self.mode)

            elif event == cv2.EVENT_LBUTTONUP:
                self.started_click = False

            elif event == cv2.EVENT_MOUSEMOVE:
                if self.started_click:
                    self.graph_maker.delete_seed(x - 1, y - 1, self.mode)

        else:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.started_click = True
                self.graph_maker.add_seed(x - 1, y - 1, self.mode)

            elif event == cv2.EVENT_LBUTTONUP:
                self.started_click = False

            elif event == cv2.EVENT_MOUSEMOVE:
                if self.started_click:
                    self.graph_maker.add_seed(x - 1, y - 1, self.mode)


    def one_image_save_seed(self):
        try:
            self.one_image_foreground_seed[self.obj_idx]
        except:
            self.one_image_foreground_seed.append(self.graph_maker.foreground_seeds)
            self.one_image_background_seed.append(self.graph_maker.background_seeds)
        else:
            self.one_image_foreground_seed[self.obj_idx] = self.graph_maker.foreground_seeds
            self.one_image_background_seed[self.obj_idx] = self.graph_maker.background_seeds