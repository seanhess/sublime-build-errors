

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

    def size(self):
        return self.panel.size()