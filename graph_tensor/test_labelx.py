from tkinter import Tk

from graph.atom import Meta
from graph.creator import Selector
from tools.labelx import Graph, LabeledGraph

def _test(test_type):
    root = Tk()
    icon_meta = Meta(root, width=210, height=60)
    icon_creator = Selector(icon_meta)
    meta = test_type(root, selector=icon_creator, background='white')
    # Makes the master widget change as the canvas size
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    meta.layout()
    icon_meta.layout(0, 1)
    root.mainloop()

def test_Graph():
    _test(Graph)

def test_LabeledGraph():
    _test(LabeledGraph)

if __name__ == '__main__':
    test_LabeledGraph()