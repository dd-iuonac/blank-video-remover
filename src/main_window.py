import threading
from tkinter import Label, Button, Spinbox, StringVar, OptionMenu

import cv2
import imutils
from PIL import ImageTk, Image


class MainWindow:

    def __init__(self, win, cap, algorithms):
        # GUI
        self.window = win
        self.algorithms = algorithms

        self.lbl1 = Label(win, text='Background Subtraction Algorithm')
        self.lbl1.place(x=50, y=20)

        self.lbl2 = Label(win, text='Median Blur Kernel')
        self.lbl2.place(x=50, y=70)

        self.lbl3 = Label(win, text='Opening Kernel')
        self.lbl3.place(x=50, y=140)

        keys = list(self.algorithms.keys())
        variable = StringVar(self.window)
        variable.set(keys[0])
        self.currentAlgorithm = keys[0]
        self.bsaMenu = OptionMenu(self.window, variable, *keys, command=self.on_algorithm_changed)
        self.bsaMenu.place(x=270, y=15)

        values = [i for i in range(1, 99, 2)]
        values.insert(0, 0)
        self.medianBlurKernel = Spinbox(bd=3, values=values)
        self.medianBlurKernel.place(x=270, y=70)

        self.openKernel = Spinbox(bd=3, values=values)
        self.openKernel.place(x=270, y=140)

        self.btnStartCamera = Button(win, text='Start Camera', command=self.start_camera)
        self.btnStartCamera.place(x=50, y=200)

        self.btnStartProcess = Button(win, text='Process', command=self.start_process)
        self.btnStartProcess.place(x=200, y=200)

        image = Image.new('RGB', (640, 480), (0, 0, 0))
        image = ImageTk.PhotoImage(image)
        self.lblImage = Label(image=image)
        self.lblImage.configure(image=image)
        self.lblImage.place(anchor='sw', relx=0.1, rely=0.9)
        self.lblMask = Label(image=image)
        self.lblMask.configure(image=image)
        self.lblMask.place(anchor='se', relx=0.9, rely=0.9)

        # Threading
        self.cap = cap
        self.frame = None
        self.processEvent = threading.Event()
        self.cameraEvent = threading.Event()
        self.cameraEvent.set()

    def on_algorithm_changed(self, algorithm):
        self.currentAlgorithm = algorithm

    def start_process(self):
        if self.processEvent.isSet():
            self.processEvent.clear()
        else:
            self.processEvent.set()

    def start_camera(self):
        if self.cameraEvent.isSet():
            self.cameraEvent.clear()
            self.window.after(30, self.video_loop)
        else:
            self.cameraEvent.set()

    def video_loop(self):
        ret, frame = self.cap.read()

        if frame.shape[0] != 480:
            self.frame = imutils.resize(frame, width=640, height=480)
        else:
            self.frame = frame

        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        self.lblImage.configure(image=image)
        self.lblImage.image = image
        if self.processEvent.isSet():
            algorithm = self.algorithms[self.currentAlgorithm]
            mask = algorithm.apply(frame)

            try:
                median_kernel = int(self.medianBlurKernel.get())
                if median_kernel % 2 == 1:
                    mask = cv2.medianBlur(mask, median_kernel)
            except ValueError:
                pass

            try:
                open_kernel = int(self.openKernel.get())
                if open_kernel > 0:
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_kernel, open_kernel))
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            except ValueError:
                pass
            mask = cv2.bitwise_not(mask)

            image = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            self.lblMask.configure(image=image)
            self.lblMask.image = image
        if not self.cameraEvent.isSet():
            self.window.after(30, self.video_loop)
