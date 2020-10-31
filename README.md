# blank-video-remover
Video surveillance - "blank sequences" removal.

Prerequisites:
- python and opencv installed on local computer,
- a video camera connected to the computer (alternatively, a pre-recorded mpeg/avi video can be used).
Specification:
Purpose: to remove (mark) video frames containing no motion ("blank sequences") from the input video stream. (e.g. it can be used to avoid unnecessary recording and processing on surveillance videos.)
Using Python and OpenCV write a program that:
- Open the video stream (e.g. by capturing video from the connected camera using cv2.VideoCapture())
- Examine in "real-time" all captured frames to:
a) Display each frame in a window as following
    - IF there is no "significant" motion between the previous frame and the current frame (black sequences) the displayed image should be marked as removed (e.g. with red diagonals over it)
    - IF some movement exists between the previous frame and the current frame the displayed image will show the unaltered content of the current frame
b) Save the current frame in an output video file only if the frame is not marked as "removed"
Obs:
 - The first frame will be captured before the process starts, and it will serve just to initiate the processing.
- The meaning of "significant motion" should be defined and refined during project implementation. Each extra variables considered here (as noise, illumination changes etc.) will be awarded with higher mark.
- No other libraries should be used except OpenCV