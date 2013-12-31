import sublime
from sublime_plugin import EventListener, WindowCommand
import os
import re
from .be_window_manager import windows
from .be_command import BuilderProcess
from .be_output_panel import OutputPanel


running_process = None

# - every time you save it sets the errors for clearing the next time you get a line
# - show errors inline in das file
# - status line: display current error
# - status: show command is running...
# - remember the command they entered last time
# - only show the error panel if they have not chosen to display the raw output

class BuildErrorsRunCommand(WindowCommand):

    def __init__(self, window):
        WindowCommand.__init__(self, window)

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
        self.settings().raw_panel = OutputPanel(self.window, "be_raw_panel")
        self.settings().raw_panel.show()
        self.settings().errors = ErrorParser()

    def on_build_line(self, line):
        # print("::", line)
        line = re.sub(r'(||>> |\[\d+m)', "", line)
        self.settings().raw_panel.write(line+"\n")
        self.settings().errors.parse(line)

        # each line, replace the error panel and display it
        self.settings().error_panel = OutputPanel(self.window, "be_error_panel")
        self.render_errors(self.settings().error_panel, self.settings().errors.errors_by_file)
        if len(self.settings().errors.errors):
            self.settings().error_panel.show()
        self.highlight_current_view()

    def on_build_exit(self):
        self.settings().raw_panel.write("\nEXITED\n")

    def settings(self):
        return windows.settings_for_window(self.window)

    def render_errors(self, panel, errors_by_file):
        root_folder = active_window_root_folder()

        regions = []
        for file, errors in errors_by_file.items():
            if len(errors) > 0:
                relative_path = os.path.relpath(file, root_folder)
                panel.write(" {0} \n".format(relative_path))

                for error in errors:
                    region_text = 'Line {0}:'.format(error.line)
                    region_start = panel.size() + 4
                    regions.append(sublime.Region(region_start, region_start + len(region_text)))
                    error_text = re.sub(re.compile('\\n', re.MULTILINE), '\\n    ', error.text)
                    panel.write('    {0} {1}\n'.format(region_text, error_text))

                panel.write('\n')

        panel.panel.add_regions('build_error', regions, 'error.line', '', sublime.DRAW_NO_FILL)

        if len(regions) == 0:
            panel.write("")

    def highlight_current_view(self):
        view = self.window.active_view()
        if not view:
            return
        highlight_view(view)


class BuildErrorsStopCommand(WindowCommand):
    def run(self):
        stop_running_process()

class BuildErrorsShowOutput(WindowCommand):
    def run(self):
        panel = windows.settings_for_window(self.window).raw_panel
        panel.show()

class BuildErrorsShowErrors(WindowCommand):
    def run(self):
        panel = windows.settings_for_window(self.window).error_panel
        panel.show()

class BuildErrorsListener(EventListener):
    def on_post_save_async(self,view):
        settings = windows.settings_for_view(view)
        settings.errors.clean()
        return

    def on_activated_async(self,view): 
        highlight_view(view)

    def on_load_async(self,view): 
        highlight_view(view)

    def on_selection_modified_async(self, view):
        if not view: return
        settings = windows.settings_for_view(view)
        if not settings: return
        errors = settings.errors.by_view(view)
        show_error_status(view, errors)

def highlight_view(view):
    settings = windows.settings_for_view(view)
    errors = settings.errors.by_view(view)
    highlight_errors(view, errors)

def highlight_errors(view, errors):
    regions = list(map(lambda e: error_region(view, e), errors))
    view.add_regions('build-error', regions, 'build.error', 'cross', sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE)

def error_region(view, error):
    a = view.text_point(error.line-1, error.column-1)
    end = view.find('\W',a) # match this whole word
    return sublime.Region(a, end.a)

def show_error_status(view, errors):
    sel = view.sel()
    (line, col) = view.rowcol(sel[0].begin())
    line_error = find_error(errors, line, view.file_name())
    if line_error:
        view.set_status("be_line", "ERROR "+line_error.text)    
    else:
        view.erase_status("be_line")

def find_error(errors, line, file):
    for error in errors:
        if error.file == file and (line+1 == error.line):
            return error
    return None

class BuildErrorsPanelSelectListener(EventListener):
    def on_selection_modified_async(self, view):
        if view.settings().get('syntax').lower().endswith('builderrorsoutput.tmlanguage'):
            error_regions = []
            error_regions.extend(view.get_regions('build_error'))

            sel_point = view.sel()[0].a
            paths = view.substr(sublime.Region(0, view.size())).split('\n')
            root_folder = active_window_root_folder()

            last_file = None
            for x in range(len(paths)):
                if paths[x].startswith('  '):
                    paths[x] = last_file
                else:
                    last_file = paths[x]

            for region in error_regions:
                if region.contains(sel_point):
                    row = view.rowcol(sel_point)[0]

                    line = int(view.substr(region)[5:-1].strip())
                    file = paths[row].strip()
                    
                    abspath = os.path.join(root_folder, file)
                    pathline = '{0}:{1}:0'.format(abspath, line)
                    window = sublime.active_window()
                    window.open_file(pathline, sublime.ENCODED_POSITION)
                    # window.focus_view(window.active_view())



class ErrorParser(object):
    def __init__(self):
        self.errors = []
        self.errors_by_file = {}
        self.err = None

    def parse(self, line):
        # TYPESCRIPT detection support
        ts = re.search('^(.+\.ts)\((\d+),(\d+)\):\s*(.*)', line)
        if ts:
            err = Error()
            err.type = "ts"
            err.file = ts.group(1)
            err.line = int(ts.group(2))
            err.column = int(ts.group(3))
            err.text = ts.group(4)
            self.start_error(err)

        # END
        elif "Exited with code" in line:
            self.end_error()

        # elif "Done, without errors" in line:
        #     self.clean()

        # APPEND ERROR
        elif self.err:
            if len(self.err.text): 
                self.err.text += "\n"
            self.err.text += line

    def clean(self):
        self.errors = []
        self.errors_by_file = {}
        self.err = None

    def start_error(self, err):
        self.end_error()
        self.err = err
        self.errors.append(err)
        self.by_file(err.file).append(err)

    def by_file(self, file):
        if not file in self.errors_by_file:
            self.errors_by_file[file] = []
        return self.errors_by_file[file]    

    def by_view(self, view):
        return self.by_file(view.file_name())

    def end_error(self):
        if self.err:
            # strip typescript error codes
            if self.err.type is 'ts':
                self.err.text = re.sub(r'error [TS0-9]+: ', '', self.err.text)
        self.err = None



class Error(object):
    def __init__(self):
        self.file = None
        self.line = None
        self.column = None
        self.text = None
        self.type = None

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
