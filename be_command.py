from threading import Thread
from subprocess import Popen, PIPE, STDOUT
import os

# can't use communicate any more, because we want to support watch commands
# need to be able to stream output
# so it needs to be on its own thread thing

class BuilderProcess(object):
    def __init__(self, command, cwd, on_line, on_exit):
        self.process = None
        self.thread = None
        self.args = command.split()
        self.on_line = on_line
        self.on_exit = on_exit
        self.cwd = cwd

    def run(self):
        kwargs = {}
        # why doesn't this work?
        env = os.environ.copy()
        env["PATH"] = '/usr/local/bin:/opt/local/bin:' + env["PATH"]
        print("!! Running", self.args, self.cwd)
        self.process = Popen(self.args, stdin=PIPE, stdout=PIPE, stderr=STDOUT, env=env, cwd=self.cwd, **kwargs)
        self.thread = Thread(target=self.read)
        self.thread.daemon = True
        self.thread.start()

    def read(self):
        print("--read--")
        # exit if we are done
        while self.process and self.process.poll() is None:
            line = self.process.stdout.readline().decode('UTF-8').rstrip()
            self.on_line(line)

        self.stopped()

    def stop(self):
        if not self.process: return
        self.process.kill()

    def stopped(self):
        self.process = None
        self.on_exit()
