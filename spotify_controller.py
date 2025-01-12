import pychromecast
from spotipy import Spotify, SpotifyOAuth
import time
import logging


logger = logging.getLogger(__name__)


class SpotifyController:
    def __init__(
        self,
        device_name,
        use_connect,
        spotify_client_id,
        spotify_client_secret,
        spotify_redirect_uri,
    ):
        """
        Initialise the SpotifyController.

        Args:
            device_name (str): The name of the device to connect to.
            use_connect (bool): Use Spotify Connect? (e.g. for Chromecasts)
            spotify_client_id (str): The Spotify App client id
            spotify_client_secret (str): The Spotify App client secret
            spotify_redirect_uri (str): The Spotify App redirect uri
        """
        self.device_name = device_name
        self.use_connect = use_connect
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.spotify_redirect_uri = spotify_redirect_uri

        self.spotify = None
        self.device = None
        self.zeroconf = None

    def run(self):
        """
        Initialise the Spotify client using the spotipy library.
        """
        try:
            self.spotify = Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=self.spotify_client_id,
                    client_secret=self.spotify_client_secret,
                    redirect_uri=self.spotify_redirect_uri,
                    scope="user-read-playback-state user-modify-playback-state",
                    open_browser=False,
                )
            )
            logger.info("Spotify client initialised successfully.")
        except Exception as e:
            logger.error(f"Failed to initialise Spotify client: {e}")
            raise

    def _discover_chromecast(self):
        """
        Discover and connect to the Chromecast device.

        Returns:
            Chromecast: The connected Chromecast instance.
        """
        logger.info("Discovering Chromecast devices...")
        chromecasts, browser = pychromecast.get_listed_chromecasts(
            friendly_names=[self.device_name]
        )
        if not chromecasts:
            logger.error(f"Chromecast named '{self.device_name}' not found.")
            raise ValueError(f"Chromecast named '{self.device_name}' not found.")

        cast = list(chromecasts)[0]
        logger.info(f"Using Chromecast: {cast.name}")
        cast.wait()  # Wait for the Chromecast to be ready
        self.device = cast
        return

    def play(self, spotify_url):
        """
        Play a Spotify URL on the device.

        Args:
            spotify_url (str): The Spotify track or playlist URL.
        """
        if self.use_connect:
            if not self.device:
                self._discover_chromecast()

            # spotify_app_id = "CC32E753"
            # self.device.quit_app()
            # self.device.start_app(spotify_app_id)
            # self.device.wait()

        # Retry mechanism to get the Spotify device ID
        retries = 100
        delay = 3  # seconds

        device_id = None
        for attempt in range(retries):
            devices = self.spotify.devices()["devices"]
            device_id = next(
                (d["id"] for d in devices if d["name"] == self.device_name), None
            )
            if device_id:
                break
            logger.info(
                f"Device '{self.device_name}' not found. Retrying... ({attempt + 1}/{retries})"
            )
            time.sleep(delay)

        if not device_id:
            logger.error(
                f"Spotify device ID for device not found after {retries} retries: {devices}"
            )
            raise ValueError("Spotify device ID for device not found.")

        try:
            logger.info(f"Playing Spotify URL: {spotify_url}")
            self.spotify.start_playback(device_id=device_id, context_uri=spotify_url)
        except Exception as e:
            logger.error(f"Failed to start playback: {e}")
            raise
