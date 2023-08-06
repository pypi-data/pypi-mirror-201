from playsound import playsound

from .config import Audio


class Sound:
    @classmethod
    def remind(cls):
        playsound(Audio.coin)

    @classmethod
    def nag(cls):
        playsound(Audio.wilhelm)
