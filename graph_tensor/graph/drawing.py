from .atom import Meta


class Drawing(Meta):
    '''Create graphic elements (graph) including rectangular boxes (which can be square points), 
        ovals (circular points), and segments.
    '''

    def __init__(self, master=None, cnf={}, selector=None, **kw):
        '''Click the left mouse button to start painting, release
            the left mouse button to complete the painting.

        :param selector: The graphics selector, which is an instance of Selector.
        '''
        super().__init__(master, cnf, **kw)
        self.master = master
        self.selector = selector
        self.master.title('Computer Vision')
        self._init_params()
        self.bind("<1>", self.update_xy)
        self.bind("<ButtonRelease-1>", self.draw)

    def _init_params(self):
        self.x = self.y = 0

    def update_xy(self, event):
        '''Press the left mouse button to record the coordinates of the left mouse button'''
        self.x = event.x
        self.y = event.y

    def get_bbox(self, event):
        x0, y0 = self.x, self.y  # The upper-left coordinates of the graph
        x1, y1 = event.x, event.y  # Lower-right coordinates of the graph
        bbox = x0, y0, x1, y1
        return bbox

    def draw(self, event):
        '''Release the left mouse button to finish painting.'''
        self.configure(cursor="arrow")
        bbox = self.get_bbox(event)
        self.create_graph(bbox)

    @property
    def graph_params(self):
        return {
            'line_width': 1,
            'tags': self.selector._graph_type,
            'fill': 'red' if 'Point' in self.selector._graph_type else None
        }

    def create_graph(self, bbox):
        '''Create a graphic.

        :param bbox: (x0,y0,x1,y1)
        '''
        x0, y0, x1, y1 = bbox
        cond1 = x0 == x1 and y0 == y1 and 'Point' not in self.selector._graph_type
        cond2 = 'Point' in self.selector._graph_type and (x0 != x1 or y0 != y1)
        if cond1 or cond2:
            return
        else:
            self.draw_graph(bbox, graph_type=self.selector.graph_type,
                            color=self.selector.color, **self.graph_params)

    def layout(self, row=0, column=0):
        '''The internal layout.'''
        self.grid(row=row, column=column, sticky='nwes')


class TrajectoryDrawing(Drawing):
    '''Draw based on the mouse's trajectory.
    '''

    def __init__(self, master=None, cnf={}, selector=None, **kw):
        super().__init__(master, cnf, selector, **kw)
        self.bind("<1>", self.update_xy)
        self.bind("<ButtonRelease-1>", self.update_xy)
        self.bind("<Button1-Motion>", self.draw)


if __name__ == '__main__':
    from tkinter import Tk
    from .creator import Selector
    root = Tk()
    icon_meta = Meta(root, width=210, height=60)
    selector = Selector(icon_meta)
    meta = Drawing(root, selector=selector, background='white')
    # Makes the master widget change as the canvas size
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    meta.layout()
    icon_meta.layout(0, 1)
    root.mainloop()
