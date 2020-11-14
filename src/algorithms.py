import cv2


class FrameDifferenceAlgorithm:
    def __init__(self, frame):
        super(FrameDifferenceAlgorithm, self).__init__()
        self.lastFrame = frame

    def apply(self, frame):
        diff = cv2.absdiff(frame, self.lastFrame)
        self.lastFrame = frame
        return cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
