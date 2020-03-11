from tkinter import Tk
from graph.creator import Selector
from graph.atom import Meta, Drawing


def test():
    root = Tk()
    icon_meta = Meta(root, width=210, height=60)
    selector = Selector(icon_meta)
    meta = Drawing(root, selector=selector, background='white')
    #meta = TrajectoryDrawing(root, selector=selector, background='white')
    # Makes the master widget change as the canvas size
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    meta.layout()
    icon_meta.layout(0, 1)
    root.mainloop()


if __name__ == '__main__':
    test()