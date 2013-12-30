from threading import Thread
from subprocess import Popen, PIPE, STDOUT

# can't use communicate any more, because we want to support watch commands
# need to be able to stream output
# so it needs to be on its own thread thing

class BuilderProcess(object):
    def __init__(self, command, cwd, on_line):
        self.process = None
        self.thread = None
        self.args = command.split()
        self.on_line = on_line
        self.cwd = cwd

    def run(self):
        print("!! Running", self.args, self.cwd)
        kwargs = {}
        self.process = Popen(self.args, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=self.cwd, **kwargs)
        self.thread = Thread(target=self.read)
        self.thread.daemon = True
        self.thread.start()

    def read(self):
        print("--read--")
        # exit if we are done
        while self.process and self.process.poll() is None:
            line = self.process.stdout.readline().decode('UTF-8').rstrip()
            self.on_line(line)

        print("!!! EXITING")
        self.process = None

    def stop(self):
        print("!!! STOPPING")
        if not self.process: return
        print("!!! STOPPED")
        self.process.kill()
        self.process = None
