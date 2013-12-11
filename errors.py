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


class TypescriptErrorPanel():

    # def __init__(self):
    #     # self.output
    #     print("HI")

    def output_create(self):
        self.output = sublime.active_window().create_output_panel('typescript_errors')
        self.output.set_syntax_file("Packages/T3S/TypescriptBuild.tmLanguage")
        self.output.settings().set("color_scheme", "Packages/T3S/TypescriptBuild.tmTheme")

    def output_open(self):
        sublime.active_window().run_command("show_panel", {"panel": "output.typescript_errors"})


    def output_close(self):
        sublime.active_window().run_command("hide_panel", {"panel": "output.typescript_errors"})


    def output_append(self, characters):
        self.output.run_command('append', {'characters': characters})

    def show_errors(self, error_list):
        print("SHOW ERRORS2", len(error_list.errors_by_file))
        self.output_create()
        self.output.set_read_only(False)

        regions = []
        for file in error_list.files():
            errors = error_list.by_file(file)
            print("file", file, len(errors))
            if not errors:
                continue

            self.output_append('{0}\n'.format(file.replace(active_window_root_folder(), "").replace("/","",1)))

            for error in errors:
                region_text = 'Line {0}:'.format(error['start']['line'] + 1)
                region_start = self.output.size() + 2
                regions.append(sublime.Region(region_start, region_start + len(region_text)))
                self.output_append('  {0} {1}\n'.format(region_text, error['text']))

            self.output_append('\n')

        self.output.add_regions('typescript-illegal', regions, 'error.line', '', sublime.DRAW_NO_FILL)
        self.output.set_read_only(True)
        self.output_open()


def active_window_root_folder():
    open_folders = sublime.active_window().folders()
    if (len(open_folders) > 0):
        return open_folders[0]
    else:
        return ""


windows = TypescriptWindowManager()
