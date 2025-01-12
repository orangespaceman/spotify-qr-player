from qr_detector import QRDetector
from spotify_controller import SpotifyController
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# load env vars
env = {
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "WARNING").upper(),
    "DEBUG_MODE": os.getenv("DEBUG_MODE", "False").lower() == "true",
    "CAMERA": int(os.getenv("CAMERA", 0)),
    "DEVICE_NAME": os.getenv("DEVICE_NAME"),
    "USE_CONNECT": os.getenv("USE_CONNECT", "False").lower() == "true",
    "SPOTIFY_CLIENT_ID": os.getenv("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_CLIENT_SECRET": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "SPOTIFY_REDIRECT_URI": os.getenv("SPOTIFY_REDIRECT_URI"),
}

logging.basicConfig(
    level=getattr(logging, env["LOG_LEVEL"], logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class Main:
    def __init__(self):
        logger.info(f"Starting application with configuration: {env}")

    def handle_qr_data(self, qr_data):
        """
        Handle decoded QR code data.

        Args:
            qr_data (str): The decoded QR code data.
        """
        logger.info(f"Action triggered for QR Code: {qr_data}")
        try:
            self.spotify_controller.play(qr_data)
        except Exception as e:
            logger.error(f"Failed to play Spotify URL: {e}")

    def run(self):
        """
        Instantiate and run
        """
        self.spotify_controller = SpotifyController(
            device_name=env["DEVICE_NAME"],
            use_connect=env["USE_CONNECT"],
            spotify_client_id=env["SPOTIFY_CLIENT_ID"],
            spotify_client_secret=env["SPOTIFY_CLIENT_SECRET"],
            spotify_redirect_uri=env["SPOTIFY_REDIRECT_URI"],
        )
        self.spotify_controller.run()

        qr_detector = QRDetector(
            debug_mode=env["DEBUG_MODE"],
            camera=env["CAMERA"],
            callback=self.handle_qr_data,
        )
        qr_detector.run()


main = Main()
main.run()
