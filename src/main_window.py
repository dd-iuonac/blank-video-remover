import os
import threading
from tkinter import Label, Frame

import cv2
from PIL import ImageTk, Image

from src.algorithm_parameters import AlgorithmParameters
from src.camera_parameters import CameraParameters
from src.settings_menu import SettingsMenu


class MainWindow:

    def __init__(self, win, cap, algorithms):
        # GUI
        self.window = win
        self.window.rowconfigure(0, minsize=250, weight=1)
        self.window.rowconfigure(1, minsize=400, weight=4)
        self.window.columnconfigure(0, minsize=300, weight=1)
        self.window.columnconfigure(1, minsize=300, weight=1)

        self.algorithms = algorithms

        self.pwAlgorithmParameters = AlgorithmParameters(master=self.window,
                                                         algorithms=self.algorithms,
                                                         text='Algorithm parameters')
        self.pwAlgorithmParameters.grid(row=0, column=0)
        self.f = Frame(master=self.window)
        self.pwCameraParameters = CameraParameters(master=self.f, text='Camera parameters', cap=cap)
        self.pwCameraParameters.pack()

        self.pwSettingsMenu = SettingsMenu(master=self.f, text='Settings')
        self.pwSettingsMenu.pack()
        self.pwSettingsMenu.btnStartCamera.bind('<Button-1>', self.on_camera_start)
        self.f.grid(row=0, column=1)

        image = Image.new('RGB', (640, 480), (0, 0, 0))
        image = ImageTk.PhotoImage(image)
        self.lblImage = Label(image=image)
        self.lblImage.configure(image=image)
        self.lblImage.grid(row=1, column=0, padx=10, pady=10)

        self.lblMask = Label(image=image)
        self.lblMask.configure(image=image)
        self.lblMask.grid(row=1, column=1, padx=10, pady=10)

        # Threading
        self.cap = cap
        self.frame = None
        self.out = None
        self.outputVideoPath = f"{os.getcwd()}/out.mp4"
        self.processEvent = threading.Event()
        self.cameraEvent = threading.Event()
        self.cameraEvent.set()

    def on_camera_start(self, param):
        if self.cameraEvent.isSet():
            self.cameraEvent.clear()
            self.window.after(30, self.video_loop)
        else:
            self.cameraEvent.set()

    def video_loop(self):
        ret, frame = self.cap.read()

        if frame.shape[0] != 480:
            self.frame = cv2.resize(frame.copy(), (640, 480))
        else:
            self.frame = frame.copy()

        algorithm = self.algorithms[self.pwAlgorithmParameters.currentAlgorithm]
        mask = algorithm.apply(frame)

        try:
            median_kernel = int(self.pwAlgorithmParameters.medianBlurKernel.get())
            if median_kernel % 2 == 1:
                mask = cv2.medianBlur(mask, median_kernel)
        except ValueError:
            pass

        try:
            open_kernel = int(self.pwAlgorithmParameters.openKernel.get())
            if open_kernel > 0:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_kernel, open_kernel))
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        except ValueError:
            pass

        if self.pwAlgorithmParameters.inverseBinaryVariable.get():
            mask = cv2.bitwise_not(mask)

        mask = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)[1]
        image = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        self.lblMask.configure(image=image)
        self.lblMask.image = image
        cnts, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_values = [cv2.contourArea(c) for c in cnts]
        maxim = max(contour_values, default=0)
        try:
            if maxim < int(self.pwAlgorithmParameters.contourThreshold.get()):
                h, w, _ = self.frame.shape
                self.frame = cv2.line(self.frame, (0, 0), (w, h), (0, 0, 255), 10)
                self.frame = cv2.line(self.frame, (0, h), (w, 0), (0, 0, 255), 10)

            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            self.lblImage.configure(image=image)
            self.lblImage.image = image
        except ValueError:
            pass
        if not self.cameraEvent.isSet():
            self.window.after(30, self.video_loop)
