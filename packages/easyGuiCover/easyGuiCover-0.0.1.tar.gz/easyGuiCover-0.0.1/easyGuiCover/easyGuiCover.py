from tkinter import *
from tkinter import filedialog
import shutil


def explorer(title=None, types=None, dir=None, where_to_copy=None):
    root = Tk()
    root.call('wm', 'attributes', '.', '-topmost', '1')
    root.withdraw()
    scr = filedialog.askopenfilename(
        initialdir=str(dir) if dir else '',
        title=str(title) if title else 'Select file', initialfile=str(types) if types else None)
    root.destroy()
    if where_to_copy and scr != '':

        path = str(shutil.copy(scr, str(where_to_copy)))
        return path
    else:
        return scr