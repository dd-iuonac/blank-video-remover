from tkinter import Label, Spinbox, StringVar
from tkinter.ttk import Labelframe

import cv2


class CameraParameters(Labelframe):
    def __init__(self, cap=None, *args, **kwargs):
        super(CameraParameters, self).__init__(*args, **kwargs)
        self.cap = cap

        var_brightness = StringVar(self)
        var_contrast = StringVar(self)
        var_sharpness = StringVar(self)
        var_exposure = StringVar(self)
        var_sharpness.set("50")
        var_exposure.set("0")
        var_contrast.set("50")
        var_brightness.set("50")

        self.lblBrightness = Label(master=self, text="Brightness")
        self.lblBrightness.grid(row=0, column=0)
        self.sbBrightness = Spinbox(master=self, from_=0, to=100, textvariable=var_brightness, command=self.on_brightness_changed)
        self.sbBrightness.grid(row=0, column=1)

        self.lblContrast = Label(master=self, text="Contrast")
        self.lblContrast.grid(row=1, column=0)
        self.sbContrast = Spinbox(master=self, from_=0, to=100, textvariable=var_contrast, command=self.on_contrast_changed)
        self.sbContrast.grid(row=1, column=1)

        self.lblSharpness = Label(master=self, text="Sharpness")
        self.lblSharpness.grid(row=2, column=0)
        self.sbSharpness = Spinbox(master=self, from_=0, to=100, textvariable=var_sharpness, command=self.on_sharpness_changed)
        self.sbSharpness.grid(row=2, column=1)

        self.lblExposure = Label(master=self, text="Exposure")
        self.lblExposure.grid(row=3, column=0)
        self.sbExposure = Spinbox(master=self, from_=-7, to=10, textvariable=var_exposure, command=self.on_exposure_changed)
        self.sbExposure.grid(row=3, column=1)

    def on_contrast_changed(self):
        self.cap.set(cv2.CAP_PROP_CONTRAST, int(self.sbContrast.get()))

    def on_brightness_changed(self):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, int(self.sbBrightness.get()))

    def on_sharpness_changed(self):
        self.cap.set(cv2.CAP_PROP_SHARPNESS, int(self.sbSharpness.get()))

    def on_exposure_changed(self):
        self.cap.set(cv2.CAP_PROP_EXPOSURE, int(self.sbExposure.get()))
