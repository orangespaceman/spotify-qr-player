from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
import numpy as np
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QRDetectorPi:
    def __init__(self, debug_mode=False, camera=0, callback=None):
        """
        Initialise the QRDetector.

        Args:
            debug_mode (bool): Whether to display debug video.
            callback (callable): A function to handle detected QR code data.
        """
        self.debug_mode = debug_mode
        self.camera = camera
        self.callback = callback if callback else self.default_callback

        self.last_triggered = None  # Last triggered QR code
        self.debounce_start_time = None  # Start time of the debounce period
        self.debounce_duration = 5  # Debounce duration in seconds

        # Initialise the picamera2
        self.picam = Picamera2()
        self.picam.configure(self.picam.create_preview_configuration())
        logger.info(f"QRDetector initialised with debug_mode={debug_mode}")

    def default_callback(self, qr_data):
        """Default callback if no custom callback is provided."""
        logger.info(f"QR Code detected: {qr_data}")

    def detect_qr_codes(self, frame):
        """
        Detect QR codes in a video frame.

        Args:
            frame (numpy.ndarray): The input video frame.

        Returns:
            list: A list of decoded QR codes.
        """
        return decode(frame)

    def process_qr_codes(self, qr_codes):
        """
        Process detected QR codes and invoke the callback.

        Args:
            qr_codes (list): List of detected QR codes.
        """
        current_time = time.time()

        if qr_codes:
            qr_data = qr_codes[0].data.decode("utf-8")

            if self.last_triggered == qr_data:
                # Restart debounce timer for the same QR code
                self.debounce_start_time = current_time
                return

            if (
                self.debounce_start_time is None
                or current_time - self.debounce_start_time >= self.debounce_duration
            ):
                self.callback(qr_data)
                self.last_triggered = qr_data
                self.debounce_start_time = current_time

    def run(self):
        """
        Start the QR code detection process.
        """
        logger.info("Starting QR code detection... Press Ctrl+C to exit.")
        self.picam.start_preview(Preview.QT if self.debug_mode else Preview.NULL)

        try:
            self.picam.start()
            while True:
                # Capture a frame from the camera
                frame = self.picam.capture_array()

                # Convert the frame to grayscale
                gray_frame = np.mean(frame, axis=2).astype(np.uint8)

                # Detect QR codes
                qr_codes = self.detect_qr_codes(gray_frame)
                self.process_qr_codes(qr_codes)

        except KeyboardInterrupt:
            logger.info("Exit signal received. Stopping...")

        finally:
            self.picam.stop()
            logger.info("Stopped QR code detection.")
