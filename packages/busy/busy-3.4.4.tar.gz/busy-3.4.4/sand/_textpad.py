import curses
from busy.util.textbox_util import NewTextbox
from curses.textpad import rectangle

# x and y represent the top corner of the rectangle. The height of the rectangle
# is always 3, so the height of the line is always 1. It always extends to the
# right edge of the parent window.

def one_line_textbox(win):
    y, x = win.getyx()
    h, w = win.getmaxyx()
    rectangle(win, y-1, x+1, y+1, w-x)
    win.refresh()
    win2 = curses.newwin(1, w-x-8, y, x+2)
    box = NewTextbox(win2)
    result = box.edit()
    # win2.getch()

def tester(fullwin):
    fullwin.move(4, 0)
    fullwin.addstr("Value:")
    result = one_line_textbox(fullwin)

curses.wrapper(tester)