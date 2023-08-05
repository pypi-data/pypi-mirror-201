import os

import pynotification

version = "0.0.0a"

install_script = os.path.join(os.path.dirname(__file__), 'lib', 'install.sh')

try:
    import cv2  # noqa
    import face_recognition  # noqa
    import playsound  # noqa
    import pvporcupine  # noqa
    import pyaudio  # noqa
except ImportError as error:
    pynotification.pynotifier(title="First time user?", dialog=True, message=f"Please run\n\n{install_script}")
    raise UserWarning(f"{error.__str__()}\n\nPlease run\n\n{install_script}")
else:
    from .main import start  # noqa
