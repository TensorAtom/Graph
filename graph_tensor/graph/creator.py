class GraphCustom:
    def __init__(self, graph_type='Rectangle', color='blue'):
        self._graph_type = graph_type
        self._color = color

    @property
    def graph_type(self):
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
        self._graph_type = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value


class SelectorMeta(GraphCustom):
    def __init__(self, meta, graph_type='Rectangle', color='blue'):
        super().__init__(graph_type, color)
        self.x, self.y = 30, 18  # 图标的起始位置
        self.color_options = 'red', 'blue', 'black', 'white', 'green'
        self.colors(meta)
        self.graphs(meta)

    @property
    def graph_elements(self):
        return {
            'Rectangle': '⬜',
            'Oval': '⚪',
            'Line': '⸺',
            'RectanglePoint': '⯀',
            'OvalPoint': '●'
        }

    @property
    def direction(self):
        '''矩形框的起始方向'''
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
        [self.graph_type_bind(meta, graph_type) for graph_type in self.graph_elements]

    def set_color(self, new_color):
        self._color = new_color

    def set_graph_type(self, new_graph_type):
        self._graph_type = new_graph_type

    def color_bind(self, canvas, color):
        canvas.tag_bind(color, '<1>',  lambda e: self.set_color(color))

    def graph_type_bind(self, canvas, graph_type):
        canvas.tag_bind(graph_type, '<1>', lambda e: self.set_graph_type(graph_type))
