from tkinter import Canvas


class Meta(Canvas):
    '''Graphic elements are composed of segments, rectangles, ellipses, and arcs.
    '''

    def __init__(self, master=None, cnf={}, **kw):
        '''The base class of all graphics frames.

        :param master: a widget of tkinter or tkinter.ttk.
        '''
        super().__init__(master, cnf, **kw)

    def layout(self):
        '''Layout graphic elements with Grid'''
        # Makes the master widget change as the canvas size
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        # Layout canvas space
        self.grid(column=0, row=0, sticky='nwes')

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
