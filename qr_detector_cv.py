import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import logging


logger = logging.getLogger(__name__)


class QRDetectorCV:
    def __init__(self, debug_mode=False, camera=0, callback=None):
        """
        Initialise the QRDetector.

        Args:
            debug_mode (bool): Whether to display debug video.
            camera (int): The camera index for video capture.
            callback (callable): A function to handle detected QR code data.
        """
        self.debug_mode = debug_mode
        self.camera = camera
        self.callback = callback

        self.last_triggered = None  # Last triggered QR code
        self.debounce_start_time = None  # Start time of the debounce period
        self.debounce_duration = 5  # Debounce duration in seconds

        logger.debug(
            f"QRDetector initialised with debug_mode={debug_mode}, camera={camera}"
        )

    def detect_qr_codes(self, frame):
        """
        Detect QR codes in a video frame.

        Args:
            frame (numpy.ndarray): The input video frame.

        Returns:
            list: A list of decoded QR codes.
        """
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return decode(gray_frame)

    def process_qr_codes(self, qr_codes):
        """
        Process detected QR codes and invoke the callback.

        Args:
            qr_codes (list): List of detected QR codes.
        """
        current_time = time.time()

        if qr_codes:
            # Use the first detected QR code
            qr_data = qr_codes[0].data.decode("utf-8")

            # If in debounce, check if the same QR code is still present
            if self.last_triggered == qr_data:
                self.debounce_start_time = current_time  # Restart debounce
                return

            # If not in debounce or debounce has elapsed, trigger the action
            if (
                self.debounce_start_time is None
                or current_time - self.debounce_start_time >= self.debounce_duration
            ):
                if self.callback:
                    self.callback(qr_data)
                self.last_triggered = qr_data
                self.debounce_start_time = current_time  # Start debounce

    def debug(self, frame, qr_codes):
        """
        Draw rectangles around detected QR codes, and display in a window.

        Args:
            frame (numpy.ndarray): The input video frame.
            qr_codes (list): List of detected QR codes.
        """
        for qr_code in qr_codes:
            points = qr_code.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array(points, dtype=np.float32))
                cv2.polylines(frame, [hull.astype(int)], True, (255, 0, 255), 3)
            else:
                cv2.polylines(
                    frame, [np.array(points, dtype=np.int32)], True, (255, 0, 255), 3
                )

        cv2.imshow("Webcam Debug Window", frame)
        cv2.waitKey(1)  # Keep window responsive

    def run(self):
        """
        Start the QR code detection process.
        """
        cap = cv2.VideoCapture(self.camera)
        logger.info("Starting QR code detection...")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.error("Failed to capture video frame. Exiting...")
                    break

                qr_codes = self.detect_qr_codes(frame)
                self.process_qr_codes(qr_codes)

                if self.debug_mode:
                    self.debug(frame, qr_codes)

        finally:
            cap.release()
            if self.debug_mode:
                cv2.destroyAllWindows()
            logger.info("Released camera, destroyed windows")
