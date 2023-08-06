from .config import system

s = system()

if s == "Linux":
    from alsaaudio import Mixer

    class VolumeControl:
        original = None

        @classmethod
        def raise_volume(cls, by=5):
            if cls.original:
                m = Mixer()
                if m.getvolume()[0] <= 100 - by:
                    m.setvolume(m.getvolume()[0] + by)
            else:
                m = Mixer()
                cls.original = m.getvolume()[0]

        @classmethod
        def restore_volume(cls):
            if cls.original:
                m = Mixer()
                m.setvolume(cls.original)
                cls.original = None


elif s == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    class VolumeControl:
        original = None
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        get_volume = volume.GetMasterVolumeLevel
        set_volume = volume.SetMasterVolumeLevel

        @classmethod
        def raise_volume(cls):
            if cls.original:
                if cls.get_volume() <= -1.0:
                    cls.set_volume(cls.get_volume() - cls.get_volume() / 2, None)
            else:
                cls.original = cls.get_volume()

        @classmethod
        def restore_volume(cls):
            if cls.original:
                cls.set_volume(cls.original, None)
