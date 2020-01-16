from tkinter import Canvas


class Meta(Canvas):
    '''Graphic elements are composed of segments, rectangles, ellipses, and arcs.
    '''

    def __init__(self, master=None, cnf={}, line_width=2, **kw):
        '''The base class of all graphics frames.
        
        :param line_width: The width of the graphic element.
        '''
        super().__init__(master, cnf, **kw)
        self.line_width = line_width

    def layout(self):
        '''Layout graphic elements with Grid'''
        # Makes the master widget change as the canvas size
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        # Layout canvas space
        self.grid(column=0, row=0, sticky='nwes')

    def draw_graph(self, direction, graph_type='Rectangle', 
                   color='blue', arc_style='arc',
                   fill=None, dash=None):
        '''Draw basic graphic elements.
        
        :param direction: Specifies the orientation of the graphic element. 
            Union[int, float] -> (x_0,y_0,x_,y_1), (x_0, y_0) refers to the starting point of 
            the reference brush (i.e., the left mouse button is pressed), and (x_1, y_1) refers to 
            the end position of the reference brush (i.e., release the left mouse button).
        :param graph_type: Types of graphic elements.
            (str) 'Rectangle', 'Oval', 'Line'(That is, segment).
        :param color: The color of the graphic element.
        :param arc_style: Style of the arc in {'arc', 'chord', or 'pieslice'}.
        :param fill: Color of the inner fill of the drawing.
        '''
        kw = {
            'width': self.line_width,
            'outline': color,
            'dash': dash
        }
        if graph_type == 'Rectangle':
            self.create_rectangle(direction, **kw)
        elif graph_type == 'Oval':
            self.create_oval(direction, **kw)
        elif graph_type == 'Arc':
            self.create_arc(direction, style=arc_style, **kw)
        elif graph_type == 'Line':
            self.create_line(direction, fill=color, width=self.line_width, dash=dash)
