from pynput import keyboard, mouse


class UserActivity:
    idle_secs = 0

    @classmethod
    def activity(cls):
        cls.idle_secs = 0

    @classmethod
    def check_idle(cls):
        cls.idle_secs += 1
        return cls.idle_secs


listener_keyboard = keyboard.Listener(
    on_press=lambda key: UserActivity.activity(),
    on_release=lambda key: UserActivity.activity(),
)
listener_keyboard.start()

listener_mouse = mouse.Listener(
    on_move=lambda x, y: UserActivity.activity(),
    on_click=lambda x, y, button, pressed: UserActivity.activity(),
    on_scroll=lambda x, y, dx, dy: UserActivity.activity(),
)
listener_mouse.start()
