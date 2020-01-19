class GraphCustom:
    '''Customize a graphic'''
    def __init__(self, graph_type='Rectangle', color='blue'):
        '''Customize a graphic

        :param graph_type: Type name of graphic object.
            (str) It contains 'Rectangle'(⬜), 'Oval'(⚪), 'Line'(⸺),
            'RectanglePoint'(⯀), 'Oval Point'(●).
        :param color: It is the color of the graph(line) of the drawing.
        '''
        self._graph_type = graph_type
        self._color = color

    @property
    def graph_type(self):
        '''Converts the type of the drawing to the type of Canvas.'''
        if 'Rectangle' in self._graph_type:
            return 'Rectangle'
        elif 'Oval' in self._graph_type:
            return 'Oval'
        elif 'Line' in self._graph_type:
            return 'Line'
        else:
            return

    @graph_type.setter
    def graph_type(self, value):
        '''Change the type of graph.'''
        self._graph_type = value

    @property
    def color(self):
        '''Sets the color of the drawing.'''
        return self._color

    @color.setter
    def color(self, value):
        '''Change the color of the drawing.'''
        self._color = value

    @property
    def graph_params(self):
        '''Set several commonly used graphics parameters.'''
        return {
            'line_width': 1,
            'tags': self._graph_type,
            'fill': 'red' if 'Point' in self._graph_type else None
        }


class SelectorMeta(GraphCustom):
    '''Sets the icon style of the graphics selector.'''
    def __init__(self, meta, graph_type='Rectangle', color='blue'):
        super().__init__(graph_type, color)
        self.x, self.y = 30, 18  # The starting position of the icon
        # Color selection list of graphics
        self.color_options = 'red', 'blue', 'black', 'white', 'green'
        self.colors(meta)
        self.graphs(meta)

    @property
    def graph_elements(self):
        '''Set several commonly used graphics parameters.'''
        return {
            'Rectangle': '⬜',
            'Oval': '⚪',
            'Line': '⸺',
            'RectanglePoint': '⯀',
            'OvalPoint': '●'
        }

    @property
    def direction(self):
        '''The starting direction of the rectangular box'''
        return self.x, self.y, self.x+20, self.y+20

    def move_color(self, k):
        return self.x+30*k, self.y-30

    def move_graph(self, k):
        x, y = self.move_color(k)
        return x, y+30

    def colors(self, meta):
        meta.create_text((self.x, self.y), text='color',
                         fill='black', font='serial 14')
        [meta.draw_graph(self.direction, 'Rectangle', 'red',
                         line_width=1, fill=color, tags=color)
         for color in self.color_options]
        [meta.move(color, *self.move_color(k))
         for k, color in enumerate(self.color_options)]

    @property
    def graph_params(self):
        return {
            'line_width': 7 if 'Line' in self._graph_type else 2,
            'tags': self._graph_type,
            'fill': 'red' if 'Point' in self._graph_type else 'white'
        }

    def graphs(self, meta, **params):
        meta.create_text((self.x, self.y+30), text='graph',
                         fill='black', font='serial 14')
        self.color = 'purple'
        for k, name in enumerate(self.graph_elements):
            self._graph_type = name
            params.update(self.graph_params)
            meta.draw_graph(self.direction,
                            graph_type=self.graph_type,
                            color=self.color, **params)
            meta.move(name, *self.move_graph(k))


class Selector(SelectorMeta):
    def __init__(self, meta, graph_type='Rectangle', color='blue'):
        super().__init__(meta, graph_type, color)
        [self.color_bind(meta, color) for color in self.color_options]
        [self.graph_type_bind(meta, graph_type)
         for graph_type in self.graph_elements]
        meta.dtag('all')

    def set_color(self, new_color):
        self._color = new_color

    def set_graph_type(self, new_graph_type):
        self._graph_type = new_graph_type

    def color_bind(self, canvas, color):
        canvas.tag_bind(color, '<1>', lambda e: self.set_color(color))

    def graph_type_bind(self, canvas, graph_type):
        canvas.tag_bind(graph_type, '<1>',
                        lambda e: self.set_graph_type(graph_type))