import cv2
import numpy as np

class WindowSink:
    def __init__(self, width: int, height: int, title="ASCII Cam"):
        self.title = title
        # The window is created, but the frame passed to write() is expected to be the correct size
        cv2.namedWindow(self.title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.title, width, height)

    def write(self, frame: np.ndarray):
        # The frame is assumed to be correctly sized by the caller.
        cv2.imshow(self.title, frame)
        # Exit on ESC key or if the window is closed by the user
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty(self.title, cv2.WND_PROP_VISIBLE) < 1:
            raise KeyboardInterrupt

    def close(self):
        cv2.destroyAllWindows()

class VirtualCamSink:
    def __init__(self, width: int, height: int, fps: int):
        import pyvirtualcam
        self.cam = pyvirtualcam.Camera(width=width, height=height, fps=fps)

    def write(self, frame):
        # pyvirtualcam expects a 3-channel (RGB) frame.
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        self.cam.send(frame)
        self.cam.sleep_until_next_frame()

    def close(self):
        self.cam.close()
