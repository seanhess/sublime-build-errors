from os import path
import sublime
import sublime_plugin
from sublime_plugin import TextCommand, EventListener, WindowCommand

class TypescriptWindowManager(object):

    def __init__(self):
        self.errors = {}

    # returns an initializes a project given a certain view
    def errors_for_view(self, view):
        if not view: return None
        return self.errors_for_window(view.window())

    def errors_for_window(self, window):
        window_id = str(window.id())

        if not (window_id in self.errors):
            self.errors[window_id] = ErrorList(window_id)

        return self.errors[window_id]

    def unload(self):
        self.errors = {}

# errors should be by WINDOW
class ErrorList():
    def __init__(self, id):
        self.id = id
        self.errors_by_file = {}
        self.count = 0
        self.extra_lines = []

    def clear(self):
        self.errors_by_file = {}
        self.extra_lines = []
        self.count = 0

    def add(self, error):
        errors = self.by_file(error.file)
        errors.append(error)
        self.count += 1

    def set_errors(self, errors):
        self.clear()
        for e in errors: self.add(e)

    def by_file(self, file):
        if not file in self.errors_by_file:
            self.errors_by_file[file] = []

        return self.errors_by_file[file]

    def files(self):
        return self.errors_by_file.keys()

    def is_empty(self):
        return (self.count == 0)

    def by_view(self, view):
        return self.by_file(view.file_name())


def active_window_root_folder():
    open_folders = sublime.active_window().folders()
    if (len(open_folders) > 0):
        return open_folders[0]
    else:
        return ""


windows = TypescriptWindowManager()
