# Run this to check if a Raspberry Pi camera can be accessed with Python
import time
from picamera2 import Picamera2, Preview
from libcamera import controls

picam = Picamera2()

# Configure for preview
config = picam.create_preview_configuration()
picam.configure(config)

# Start the preview
picam.start_preview(Preview.QT)
picam.set_controls({"AfMode": controls.AfModeEnum.Continuous})

picam.start()

time.sleep(10)

picam.close()
