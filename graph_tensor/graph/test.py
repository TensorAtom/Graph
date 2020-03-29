from tkinter import Tk


def test_Meta():
    from .atom import Meta
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    self = Meta(root)
    kw = {
        'color': 'purple',
        'dash': 2,
        'width': 2,
        'tags': 'test '
    }
    self.draw_graph('line', [20, 20, 100, 200], **kw)
    self.draw_graph('oval', [50, 80, 100, 200], fill='red', **kw)
    self.draw_graph('rectangle', [170, 80, 220, 200], fill='yellow', **kw)
    self.draw_graph('arc', [180, 100, 250, 260],
                    fill='lightblue', style='chord', **kw)
    self.draw_graph('polygon', [(70, 80), (20, 70), (30, 90)], fill='purple', **kw)
    self.layout(row=0, column=0)
    print(self.gettags(1))
    print(self.find_withtag('graph'))
    root.mainloop()


def test_Drawing():
    from .atom import Drawing
    from .creator import SelectorFrame
    root = Tk()
    selector = SelectorFrame(root)
    # or TrajectoryDrawing
    meta = Drawing(root, selector, background='lightgray')
    # Makes the master widget change as the canvas size
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    meta.layout()
    selector.layout()
    selector.grid(row=0, column=1, sticky='nwes')
    root.mainloop()


def test_GraphWindow():
    from .atom import GraphScrollable
    from .creator import SelectorFrame
    from .window import Window
    root = Window()
    root.geometry('600x800')
    selector = SelectorFrame(root)
    graph = GraphScrollable(root, selector, background='lightgray')
    root.update_edit_menu(graph)
    root.update_file_menu(graph)
    # Makes the master widget change as the canvas size
    graph.layout()
    selector.layout()
    selector.pack(side='right', fill='y')
    root.mainloop()
