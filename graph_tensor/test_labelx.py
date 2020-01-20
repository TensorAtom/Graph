from tkinter import Tk


def test():
    from graph.atom import Meta
    from graph.creator import Selector
    from tools.labelx import Graph
    root = Tk()
    icon_meta = Meta(root, width=210, height=60)
    icon_creator = Selector(icon_meta)
    meta = Graph(root, selector=icon_creator, background='white')
    # Makes the master widget change as the canvas size
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    meta.layout()
    icon_meta.layout(0, 1)
    root.mainloop()

if __name__ == '__main__':
    test()