from tkinter import Label, Spinbox
from tkinter.ttk import Labelframe

import cv2


class CameraParameters(Labelframe):
    def __init__(self, cap=None, *args, **kwargs):
        super(CameraParameters, self).__init__(*args, **kwargs)
        self.cap = cap

        self.lblBrightness = Label(master=self, text="Brightness")
        self.lblBrightness.grid(row=0, column=0)
        self.sbBrightness = Spinbox(master=self, from_=0, to=100, command=self.on_brightness_changed)
        self.sbBrightness.grid(row=0, column=1)

        self.lblContrast = Label(master=self, text="Contrast")
        self.lblContrast.grid(row=1, column=0)
        self.sbContrast = Spinbox(master=self, from_=0, to=100, command=self.on_contrast_changed)
        self.sbContrast.grid(row=1, column=1)

    def on_contrast_changed(self):
        self.cap.set(cv2.CAP_PROP_CONTRAST, int(self.sbContrast.get()))

    def on_brightness_changed(self):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, int(self.sbBrightness.get()))
