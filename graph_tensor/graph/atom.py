from tkinter import Canvas, StringVar, ttk


class Meta(Canvas):
    '''Graphic elements are composed of segments, rectangles, ellipses, and arcs.
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

    def draw_graph(self, direction, graph_type='Rectangle',
                   color='blue', line_width=1, arc_style='arc',
                   tags=None, fill=None, dash=None):
        '''Draw basic graphic elements.

        :param direction: Specifies the orientation of the graphic element. 
            Union[int, float] -> (x_0,y_0,x_,y_1), (x_0, y_0) refers to the starting point of 
            the reference brush (i.e., the left mouse button is pressed), and (x_1, y_1) refers to 
            the end position of the reference brush (i.e., release the left mouse button).
        :param graph_type: Types of graphic elements.
            (str) 'Rectangle', 'Oval', 'Line'(That is, segment).
        :param color: The color of the graphic element.
        :param line_width: The width of the graphic element.(That is, center fill)
        :param arc_style: Style of the arc in {'arc', 'chord', or 'pieslice'}.
        :param fill: Color of the inner fill of the drawing.
        :return: Unique identifier solely for graphic elements.
        '''
        kw = {
            'width': line_width,
            'outline': color,
            'dash': dash,
        }
        tag_collect = {'graph'}
        if tags is not None:
            tag_collect.add(tags)
        if graph_type == 'Rectangle':
            tag_collect.add('rectangle')
            graph_id = self.create_rectangle(
                direction, tags=tuple(tag_collect),
                fill=fill, **kw)
        elif graph_type == 'Oval':
            tag_collect.add('oval')
            graph_id = self.create_oval(
                direction, tags=tuple(tag_collect),
                fill=fill, **kw)
        elif graph_type == 'Arc':
            tag_collect.add('arc')
            graph_id = self.create_arc(
                direction, style=arc_style,
                tags=tuple(tag_collect),
                fill=fill, **kw)
        elif graph_type == 'Line':
            tag_collect.add('line')
            graph_id = self.create_line(direction, fill=color,
                                        width=line_width,
                                        tags=tuple(tag_collect), dash=dash)
        else:
            graph_id = None
        return graph_id


class Drawing(Meta):
    '''Create graphic elements (graph) including rectangular boxes (which can be square points), 
        ovals (circular points), and segments.
    '''

    def __init__(self, home, selector, cnf={}, **kw):
        '''Click the left mouse button to start painting, release
            the left mouse button to complete the painting.

        :param selector: The graphics selector, which is an instance of graph.creator.Selector.
        '''
        super().__init__(home, cnf, **kw)
        self.home = home # Instance of ttk.Frame
        self.coord_var = StringVar()
        self.coord_label = ttk.Label(self.home, textvariable = self.coord_var)
        self.selector = selector
        self._init_params()
        self._draw_bind()

    def layout(self):
        self.pack(side='top', expand='yes', fill='both')
        self.coord_label.pack(side='bottom', anchor='w')
        
    def _draw_bind(self):
        self.selector.graph_type = 'Rectangle'
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
        self.coord_var.set(f'coordinate: {bbox[:2]} to {bbox[2:]}')

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


class TrajectoryDrawing(Drawing):
    '''Draw based on the mouse's trajectory.
    '''

    def __init__(self, master=None, cnf={}, selector=None, **kw):
        super().__init__(master, cnf, selector, **kw)
        self.bind("<1>", self.update_xy)
        self.bind("<ButtonRelease-1>", self.update_xy)
        self.bind("<Button1-Motion>", self.draw)
