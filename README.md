- Allows you to run any terminal command in a panel. 
- Displays the full output, 
- Displays a list of the errors found
- Highlight errors inline

TODO
----

- specify a command to run
- show the full output of the command in a window
- show/hide the window

"no way to intercept a real build script"
- set the command to run / run it in project settings
- sublime command: run/restart the build. + key stroke
- sublime command: show the full output
- automatically show the errors 
- sublime to re-show the current error output

- ability to set the command to run for the build (a build script?)
- run it.. when? when you hit build?
- there's no way to intercept the actual build scrope

Now here's the issue. When they save a file, it might update again.

Simplish: start the build, grab all errors on DONE, then show again
Harder: wait for the build to "stabilize", then show errors
    - if there is no output for 500 ms?... eh... not really
    - on save, reset
    - wait... stuff .... wait  wait ... stuff
    - each time "stuff" is hit, then erase the window and show errors?

