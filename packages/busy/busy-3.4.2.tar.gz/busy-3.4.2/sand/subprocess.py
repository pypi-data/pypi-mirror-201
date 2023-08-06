# Can I invoke ZSH in a subprocess?

import subprocess

# Implements the full command
subprocess.run(['ls', '-al'])

# Does ls but no options
print()
subprocess.run(['ls', '-al'], shell=True)

# Gives "zsh: can't open input file: ls"
print()
subprocess.run(['zsh', 'ls', '-al'])

# zsh: can't open input file: "ls -al"
print()
subprocess.run(['zsh', '"ls -al"'])

# Another error
print()
subprocess.run("zsh ls -al", shell=True)

# Works as expected
print()
subprocess.run("ls -al", shell=True)

# && works
print()
subprocess.run("ls -al && ls -al", shell=True)

# !$ doesn't work - we're in /bin/sh
print()
subprocess.run("ls -al && echo \"!$\"", shell=True)

# So this doesn't work either
print()
subprocess.run("l", shell=True)

# This calls ZSH, but doesn't get .zshrc
print()
subprocess.run("l", shell=True, executable="/bin/zsh")

# Still doesn't work
print()
subprocess.run("ls -al && echo \"!$\"", shell=True, executable="/bin/zsh")

# Back to sh, try our own command - this works
print()
subprocess.run("busy list", shell=True)

# But it also works in a list? Yes
print()
subprocess.run(["busy", "list"])

# But now we can't use &&, so shell is better
print()
subprocess.run(["busy", "list", "&&", "busy", "list"])

# Can we get variables from .zshrc? Maybe if already set
print()
subprocess.run("echo $EDITOR", shell=True)
