Sublime Build Errors
--------------------

- Allows you to run any terminal command from sublime
- Displays the output of that command
- If errors are found, displays them in a panel, and highlights them in the editor

Installation
------------

Go to your packages folder in Terminal.

    cd Library/Application Support/Sublime Text 3/Packages

Clone this repository into that folder

    git clone https://github.com/seanhess/sublime-build-errors

Usage
-----

Right now, everything is in `Tools -> Command Palette`. First run the following command:

    BuildErrors: Run Command

It will prompt you to enter a command. Edit and hit enter. It will show you the raw output, then if it encounters any errors will display the errors in a panel. 




