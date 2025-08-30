import cv2
import threading

class ThreadedCamera:
    """
    A wrapper for a cv2.VideoCapture object that reads frames in a separate thread.
    This prevents the main thread from blocking on I/O and ensures the latest frame
    is always available.
    """
    def __init__(self, index: int, width: int, height: int, fps: int):
        self.cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
        if not self.cap.isOpened():
            raise RuntimeError(f"camera {index} not opened")

        # Set desired camera properties (best-effort)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        # Read the first frame to ensure the camera is working
        self.grabbed, self.frame = self.cap.read()
        if not self.grabbed:
            self.cap.release()
            raise RuntimeError("camera read failed on initial frame")

        self.stopped = False
        self.lock = threading.Lock()

        # Start the thread to read frames from the video stream
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        """Thread target function that continuously reads frames."""
        while not self.stopped:
            grabbed, frame = self.cap.read()
            if not grabbed:
                # If we fail to grab a frame, stop the thread.
                self.stopped = True
                continue
            with self.lock:
                self.frame = frame

    def read(self):
        """Return the most recent frame."""
        if self.stopped:
            return None
        with self.lock:
            # Return a copy to prevent race conditions if the caller modifies the frame
            return self.frame.copy()

    def release(self):
        """Stop the thread and release video capture resources."""
        self.stopped = True
        self.thread.join()  # Wait for the thread to finish
        self.cap.release()


def open_capture(index: int, width: int, height: int, fps: int):
    """Opens a camera capture using the threaded reader."""
    return ThreadedCamera(index, width, height, fps)


def read_frame(capture_obj):
    """Reads a frame from the threaded capture object."""
    frame = capture_obj.read()
    if frame is None:
        raise RuntimeError("camera read failed or stream ended")
    return frame


def list_indexes(max_try: int = 10):
    """Lists available camera indexes."""
    found = []
    for i in range(max_try):
        c = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
        if c.isOpened():
            found.append(i)
            c.release()
    return found
