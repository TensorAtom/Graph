
from tkinter import Canvas


class Meta(Canvas):
    '''Graphic elements are composed of line(segment), rectangle, ellipse, and arc.
    '''

    def __init__(self, master=None, cnf={}, **kw):
        '''The base class of all graphics frames.

        :param master: a widget of tkinter or tkinter.ttk.
        '''
        super().__init__(master, cnf, **kw)

    def layout(self, row=0, column=0):
        '''Layout graphic elements with Grid'''
        # Layout canvas space
        self.grid(row=row, column=column, sticky='nwes')

    def draw_graph(self, graph_type, direction, color='blue', width=1, tags=None, **kwargs):
        '''Draw basic graphic elements.

        :param direction: Specifies the orientation of the graphic element. 
            Union[int, float] -> (x_0,y_0,x_,y_1), (x_0, y_0) refers to the starting point of 
            the reference brush (i.e., the left mouse button is pressed), and (x_1, y_1) refers to 
            the end position of the reference brush (i.e., release the left mouse button).
        :param graph_type: Types of graphic elements.
            (str) 'rectangle', 'oval', 'line', 'arc'(That is, segment).
            Note that 'line' can no longer pass in the parameter 'fill', and 
            the remaining graph_type cannot pass in the parameter 'outline'.
        :param color: The color of the graphic element.
        :param width: The width of the graphic element.(That is, center fill)
        :param tags: The tags of the graphic element. 
            It cannot be a pure number (such as 1 or '1' or '1 2 3'), it can be a list, a tuple, 
            or a string separated by a space(is converted to String tupers separated by a blank space). 
            The collection or dictionary is converted to a string.
            Example:
                ['line', 'graph'], ('test', 'g'), 'line',
                ' line kind '(The blanks at both ends are automatically removed), and so on.
        :param style: Style of the arc in {'arc', 'chord', or 'pieslice'}.

        :return: Unique identifier solely for graphic elements.
        '''
        com_kw = {'width': width, 'tags': tags}
        kw = {**com_kw, 'outline': color}
        line_kw = {**com_kw, 'fill': color}

        if graph_type == 'line':
            kwargs.update(line_kw)
        else:
            kwargs.update(kw)
        if graph_type in ('rectangle', 'oval', 'line', 'arc'):
            func = eval(f"self.create_{graph_type}")
            graph_id = func(direction, **kwargs)
            if tags is None:
                [self.addtag_withtag(tag, graph_id)
                 for tag in ('graph', graph_type)]
        else:
            graph_id = None
        return graph_id


class Drawing(Meta):
    '''Create graphic elements (graph) including rectangular boxes (which can be square points), 
        ovals (circular points), and segments.
    '''

    def __init__(self, master=None, selector=None, cnf={}, **kw):
        '''Click the left mouse button to start painting, release
            the left mouse button to complete the painting.

        :param selector: The graphics selector, which is an instance of Selector.
        '''
        super().__init__(master, cnf, **kw)
        self.selector = selector

        self._init_params()
        self._draw_bind()

    def _draw_bind(self):
        self.bind("<1>", self.update_xy)
        self.bind("<ButtonRelease-1>", self.draw)

    def _init_params(self):
        self.x = self.y = 0

    def update_xy(self, event):
        '''Press the left mouse button to record the coordinates of the left mouse button'''
        self.x = self.canvasx(event.x)
        self.y = self.canvasy(event.y)

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

    def create_graph(self, bbox):
        '''Create a graphic.

        :param bbox: (x0,y0,x1,y1)
        '''
        x0, y0, x1, y1 = bbox
        cond1 = x0 == x1 and y0 == y1 and 'point' not in self.selector.graph_type
        cond2 = 'point' in self.selector.graph_type and (x0 != x1 or y0 != y1)
        if cond1 or cond2:
            return
        else:
            self.draw_graph(self.selector.graph_type.split('_')
                            [0], bbox, self.selector.color)

    def layout(self, row=0, column=0):
        '''The internal layout.'''
        self.grid(row=row, column=column, sticky='nwes')


class TrajectoryDrawing(Drawing):
    '''Draw based on the mouse's trajectory.
    '''

    def __init__(self, master,  selector, cnf={}, **kw):
        super().__init__(master, selector, cnf, **kw)
        self.bind("<1>", self.update_xy)
        self.bind("<ButtonRelease-1>", self.update_xy)
        self.bind("<Button1-Motion>", self.draw)


class GraphMeta(Drawing):
    def __init__(self, master,  selector, cnf={}, **kw):
        super().__init__(master, selector, cnf, **kw)