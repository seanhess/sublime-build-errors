

# Separate Settings Per Window
class WindowManager(object):
    def __init__(self):
        self.settings = {}

    def settings_for_view(self, view):
        if not view: return None
        return self.settings_for_window(view.window())

    def settings_for_window(self, window):
        if not window: return None
        window_id = str(window.id())

        if not (window_id in self.errors):
            self.settings[window_id] = Settings()

        return self.settings[window_id]

    def unload(self):
        self.settings = {}


class Settings(object):
    def __init__(self):
        self.command = None

windows = WindowManager()