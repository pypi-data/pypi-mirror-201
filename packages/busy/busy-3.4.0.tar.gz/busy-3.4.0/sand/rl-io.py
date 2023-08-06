# Can I override stdin or stdout for readline/input? I guess not.

import readline
from contextlib import redirect_stdout
from io import StringIO


with redirect_stdout(StringIO()) as f:
    print("Hello")
    readline.parse_and_bind('tab: complete')
    input()
print(f.getvalue())