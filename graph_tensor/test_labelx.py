from tkinter import Tk

from graph.atom import Meta
from graph.creator import Selector
from tools.labelx import Graph, LabeledGraph

def _test(root, test_type):
    icon_meta = Meta(root, width=210, height=60)
    icon_creator = Selector(icon_meta)
    meta = test_type(root, selector=icon_creator, background='white')
    # Makes the master widget change as the canvas size
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    meta.layout()
    icon_meta.layout(0, 1)
    return meta

def test_Graph():
    root = Tk()
    _test(root, Graph)
    root.mainloop()

def test_LabeledGraph():
    root = LabeledGraph()
    root.mainloop()


if __name__ == '__main__':
    #test_Graph()
    test_LabeledGraph()