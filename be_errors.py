import re


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
