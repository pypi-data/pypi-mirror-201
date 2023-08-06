from os import system as os_system

from .config import system
from .lang import L

s = system()

if s == "Linux":

    class PowerManagement:
        @classmethod
        def system_poweroff(cls):
            os_system("systemctl poweroff")

        @classmethod
        def system_suspend(cls):
            os_system("systemctl suspend")

        @classmethod
        def system_hibernate(cls):
            os_system("systemctl hibernate")

        @classmethod
        def system_hybrid_sleep(cls):
            os_system("systemctl hybrid-sleep")

        @classmethod
        def system_suspend_then_hibernate(cls):
            os_system("systemctl suspend-then-hibernate")

    SYSTEM_COMMANDS = {
        L.PWRMNGMT_A_POWEROFF: PowerManagement.system_poweroff,
        L.PWRMNGMT_A_SUSPEND: PowerManagement.system_suspend,
        L.PWRMNGMT_A_HIBERNATE: PowerManagement.system_hibernate,
        L.PWRMNGMT_A_HS: PowerManagement.system_hybrid_sleep,
        L.PWRMNGMT_A_STH: PowerManagement.system_suspend_then_hibernate,
    }


elif s == "Windows":

    class PowerManagement:
        @classmethod
        def system_poweroff(cls):
            os_system("shutdown /s /t 0")

        @classmethod
        def system_suspend(cls):
            os_system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    SYSTEM_COMMANDS = {
        L.PWRMNGMT_A_POWEROFF: PowerManagement.system_poweroff,
        L.PWRMNGMT_A_SUSPEND: PowerManagement.system_suspend,
    }
