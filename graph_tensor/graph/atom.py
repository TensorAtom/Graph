'''Some of the actions related to the graph.
'''
from tkinter import Canvas, StringVar, ttk


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
        Press the left mouse button to start painting, release the left 
            mouse button for the end of the painting.
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
        

class Graph(Drawing):
    def __init__(self, master,  selector, cnf={}, **kw):
        super().__init__(master, selector, cnf, **kw)
        self.selected_tags = None
        self.edit_var = StringVar()

    @property
    def tags_dict(self):
        return {
            'Single element': 'current',
            'All elements': 'all',
            'All graphic elements': 'graph',
            '⬜': 'rectangle',
            '⚪': 'oval',
            '⸺': 'line',
            '⯀': 'rectangle_point',
            '●': 'oval_point'
        }

    def move_strides(self, event):
        x, y = self.x, self.y
        self.update_xy(event)
        x_move = self.x - x
        y_move = self.y - y
        return x_move, y_move

    def move_graph(self, event):
        x_move, y_move = self.move_strides(event)
        self.move(self.selected_tags, x_move, y_move)

    def delete_graph(self, event):
        self.delete(self.selected_tags)

    def select_graph(self, event, edit_option):
        self.configure(cursor="target")
        self.update_xy(event)
        tags = self.tags_dict[edit_option]
        if tags == 'current':
            self.selected_tags = self.find_withtag(tags)
        else:
            self.selected_tags = tags

    def bind_graph(self):
        self.unbind('<ButtonRelease-1>')
        self.unbind('<1>')
        edit = self.edit_var.get()
        if edit == 'drawing':
            self._draw_bind() # reset bind
        elif 'move' in edit:
            self.bind('<1>', lambda event: self.select_graph(
                event, edit.split('/')[1]))
            self.bind('<ButtonRelease-1>', self.move_graph)
        elif 'delete' in edit:
            self.bind('<1>', lambda event: self.select_graph(
                event, edit.split('/')[1]))
            self.bind('<ButtonRelease-1>', self.delete_graph)


class GraphLabeled(Graph):
    '''Pin the picture and label it on it.
    '''
    def __init__(self, master,  selector, cnf={}, **kw):
        super().__init__(master, selector, cnf, **kw)
        self._set_scroll()
        self.configure(width=800, height=600)
        self.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.bind("<3>", self.mouse_motion)

    def select_graph(self, event, edit_option):
        self.configure(cursor="target")
        self.update_xy(event)
        tags = self.tags_dict[edit_option]
        image_tags = self.find_withtag('image')
        selected_tags = self.find_withtag(tags)
        self.selected_tags = set(selected_tags) - set(image_tags)

    def move_graph(self, event):
        x_move, y_move = self.move_strides(event)
        for tag in self.selected_tags:
            self.move(tag, x_move, y_move)

    def delete_graph(self, event):
        for tag in self.selected_tags:
            self.delete(tag)

    def _set_scroll(self):
        self.scroll_x = ttk.Scrollbar(self, orient='horizontal')
        self.scroll_y = ttk.Scrollbar(self, orient='vertical')

    def mouse_motion(self, event):
        x = event.x
        y = event.y
        text = f"coordinate: ({x}, {y})|| {self.canvas.canvasx(x), self.canvas.canvasy(y)}"
        self.canvas.coord_var.set(text)

    def _scroll_command(self):
        self.scroll_x['command'] = self.canvas.xview
        self.scroll_y['command'] = self.canvas.yview

    def layout(self):
        self.scroll_x.pack(side='top', fill='x')
        self.pack(side='left', expand='yes', fill='both')
        self.scroll_y.pack(side='right', fill='y')