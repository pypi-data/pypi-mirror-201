import sys

name = "tello_solectric_pl"
if sys.version_info < (3, 8, 0):
    print(f"Niestety - Twoja wersja Pythona ({sys.version}) jest zbyt niska! Zainstaluj przynajmniej 3.8 !")
    sys.exit(1)

print(f"Twoja wersja Pythona ({sys.version}) jest OK.")
from .tello_solectric_pl import *