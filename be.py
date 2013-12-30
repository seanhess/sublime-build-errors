import sublime
from sublime_plugin import EventListener, WindowCommand
import os
import re
from .be_window_manager import windows
from .be_command import BuilderProcess


running_process = None

# I need a way to stop all existing window commands!
# like a global variable thing
# but it won't automatically unload ones when the plugin reloads :(
# I just lose references to them

class BuildErrorsRunCommand(WindowCommand):

    def __init__(self, window):
        WindowCommand.__init__(self, window)
        self.full_output = None

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
        process = BuilderProcess(command, active_window_root_folder(), self.on_build_line)
        process.run()
        running_process = process
        self.full_output = OutputPanel(self.window, "be_full_output")
        self.full_output.show()

    def on_build_line(self, line):
        line = line.replace("", "") # Terminal bell. I could play a sound or something?
        line = line.replace("[39m", "")  # End of color
        line = line.replace("[32m", " √ ") # Green
        line = line.replace("[33m", " ! ") # Yellow
        line = line.replace("[31m", " ! ") # Red
        line = line.replace("[36m", " - ") # blue
        line = line.replace("[4m", "# ") # underline
        line = line.replace("[24m", "") # End of a line? End Underline?
        # line = line.replace("", "") # remove any 

        print("-:", line)
        self.full_output.write(line+"\n")


class BuildErrorsStopCommand(WindowCommand):
    def run(self):
        stop_running_process()



# # Running "watch" task
# Waiting...•OK
# >> File "test/test.ts" changed.

# # Running "exec:compile" (exec) task
# !>> /Users/seanhess/projects/sublime-build-errors/test/test.ts(1,5):
# !>> error TS2011: Cannot convert 'number' to 'string'.
# !>> Exited with code: 1.
# !Warning: Task "exec:compile" failed. Use --force to continue.•

# !Aborted due to warnings.•
# Completed in 1.885s at Mon Dec 30 2013 15:10:41 GMT-0700 (MST)• - Waiting...


class OutputPanel(object):

    def __init__(self, window, name):
        self.window = window
        self.panel = window.create_output_panel(name)
        self.name = name
        self.panel.settings().set("color_scheme", "Packages/sublime-build-errors/theme/BuildErrors.tmTheme")
        self.panel.set_syntax_file("Packages/sublime-build-errors/theme/BuildErrorsOutput.tmLanguage")

    def show(self):
        self.window.run_command("show_panel", {"panel": "output."+self.name}) 

    def hide(self):
        self.window.run_command("hide_panel", {"panel": "output."+self.name})        

    def write(self, characters):
        self.panel.set_read_only(False)
        self.panel.run_command('append', {'characters': characters})
        self.panel.set_read_only(True)

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