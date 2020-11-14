from tkinter import Tk

import cv2

from src.algorithms import FrameDifferenceAlgorithm
from src.main_window import MainWindow

cap = cv2.VideoCapture(0)
_, frame = cap.read()

algorithms = {
    "Frame Difference": FrameDifferenceAlgorithm(frame),
    "MOG": cv2.bgsegm.createBackgroundSubtractorMOG(),
    "MOG2": cv2.createBackgroundSubtractorMOG2(),
    "KNN": cv2.createBackgroundSubtractorKNN(),
    "CNT": cv2.bgsegm.createBackgroundSubtractorCNT(),
    "GMG": cv2.bgsegm.createBackgroundSubtractorGMG(),
    "LSBP": cv2.bgsegm.createBackgroundSubtractorLSBP(),
    "GSOC": cv2.bgsegm.createBackgroundSubtractorGSOC()
}

window = Tk()
mywin = MainWindow(window, cap, algorithms)
window.state('zoomed')
window.title('Video blank remover')
window.geometry("1000x700+10+10")
window.mainloop()
cap.release()
