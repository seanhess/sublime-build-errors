import sublime
from sublime_plugin import EventListener, WindowCommand
import os
import re
from .be_window_manager import windows
from .be_command import BuilderProcess
from .be_output_panel import OutputPanel


running_process = None

# - every time you save it sets the errors for clearing the next time you get a line
# - 

class BuildErrorsRunCommand(WindowCommand):

    def __init__(self, window):
        WindowCommand.__init__(self, window)
        self.raw_panel = None
        self.errors = None
        self.errors_panel = None

    def run(self):
        self.window.show_input_panel("Please enter your build command:", "grunt", self.on_input_done, self.on_input_change, self.on_input_cancel)

    def on_input_done(self, input):
        self.run_command(input)

    def on_input_change(self, input):
        return

    def on_input_cancel(self):
        return

    def run_command(self, command):
        global running_process
        stop_running_process()
        if ("grunt" in command):
            command += " --no-color"
        process = BuilderProcess(command, active_window_root_folder(), self.on_build_line, self.on_build_exit)
        process.run()
        running_process = process
        self.raw_panel = OutputPanel(self.window, "be_raw_panel")
        self.raw_panel.show()
        self.settings().raw_panel = self.raw_panel
        self.errors = ErrorParser(self.on_error)

    def on_build_line(self, line):
        # print("::", line)
        line = re.sub(r'(||>> |\[\d+m)', "", line)
        self.raw_panel.write(line+"\n")
        self.errors.parse(line)

    def on_build_exit(self):
        self.raw_panel.write("\nEXITED\n")

    def settings(self):
        return windows.settings_for_window(self.window)

    def on_error(self, err):
        self.errors_panel = OutputPanel(self.window, "be_errors_panel")
        # write out ALL errors here
        for err in self.errors.errors:
            self.errors_panel.write("\n"+err.file+":"+err.text)
        self.errors_panel.show()
        self.settings().errors_panel = self.errors_panel




class BuildErrorsStopCommand(WindowCommand):
    def run(self):
        stop_running_process()


class BuildErrorsShowOutput(WindowCommand):
    def run(self):
        panel = windows.settings_for_window(self.window).raw_panel
        panel.show()

class BuildErrorsShowErrors(WindowCommand):
    def run(self):
        panel = windows.settings_for_window(self.window).errors_panel
        panel.show()


class ErrorParser(object):
    def __init__(self, on_error):
        self.errors = []
        self.err = None
        self.on_error = on_error

    def parse(self, line):

        # TYPESCRIPT detection support
        ts = re.search('^(\/.*\.ts)\((\d+),(\d+)\):\s*(.*)', line)
        if ts:
            err = Error()
            err.file = ts.group(1)
            err.line = int(ts.group(2))
            err.column = int(ts.group(3))
            err.text = ts.group(4)
            self.start_error(err)

        # END
        elif "Exited with code" in line:
            self.end_error()

        # APPEND ERROR
        elif self.err:
            if len(self.err.text): 
                self.err.text += "\n"
            self.err.text += line

    def start_error(self, err):
        self.end_error()
        self.err = err
        self.errors.append(err)

    def end_error(self):
        if self.err:
            self.on_error(self.err)
        self.err = None




class Error(object):
    def __init__(self):
        self.file = None
        self.line = None
        self.column = None
        self.text = None

    def __repr__(self):
        return self.file+"("+str(self.line)+","+str(self.column)+"): "+self.text

def active_window_root_folder():
    window = sublime.active_window()
    project_file = window.project_file_name()
    if project_file: return os.path.dirname(project_file)

    open_folders = sublime.active_window().folders()
    if (len(open_folders) > 0):
        return open_folders[0]
    else:
        return ""


def plugin_loaded():
    return

def plugin_unloaded():
    stop_running_process()

def stop_running_process():
    global running_process
    if (running_process):
        running_process.stop()
    running_process = None
