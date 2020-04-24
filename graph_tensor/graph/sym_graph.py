from sympy import Interval


from sympy import Interval


class Rectangle(dict):
    def __init__(self, bbox, *args, **kw):
        '''
        scope_names = {'bottom_left_corner',
            'bottom_right_corner',
            'bottom_side',
            'left_side',
            'right_side',
            'top_left_corner',
            'top_right_corner',
            'top_side'}
        '''
        super().__init__(*args, **kw)
        self.__dict__ = self
        self.bbox = bbox
        self.x0, self.y0, self.x1, self.y1 = self.bbox
    
    def get_scope(self, point, radius):
        for name in self.scope_names:
            scope_str = f"self.{name}"
            if point in  eval(scope_str)(radius):
                return name
        return 
    
    @property
    def x_interval(self):
        return Interval(self.x0, self.x1)
    
    @property
    def y_interval(self):
        return Interval(self.y0, self.y1)

    @property
    def w(self):
        return self.x_interval.measure + 1

    @property
    def h(self):
        return self.y_interval.measure + 1

    @property
    def aspect_ratio(self):
        return self.w /self.h
    
    def top_left_corner(self, radius):
        x_scope = Interval.Ropen(self.x0, self.x0+radius)
        y_scope = Interval.Ropen(self.y0, self.y0+radius)
        return x_scope * y_scope
    
    def top_right_corner(self, radius):
        x_scope = Interval.Lopen(self.x1-radius, self.x1)
        y_scope = Interval.Lopen(self.y0, self.y0+radius)
        return x_scope * y_scope

    def bottom_left_corner(self, radius):
        x_scope = Interval.Ropen(self.x0, self.x0+radius)
        y_scope = Interval.Ropen(self.y1-radius, self.y1)
        return x_scope * y_scope
    
    def bottom_right_corner(self, radius):
        x_scope = Interval.Lopen(self.x1-radius, self.x1)
        y_scope = Interval.Lopen(self.y1-radius, self.y1)
        return x_scope * y_scope
    
    def left_side(self, radius):
        x_scope = Interval.Ropen(self.x0, self.x0+radius)
        y_scope = Interval.open(self.y0+radius, self.y1-radius)
        return x_scope * y_scope
    
    def right_side(self, radius):
        x_scope = Interval.Lopen(self.x1-radius, self.x1)
        y_scope = Interval.open(self.y0+radius, self.y1-radius)
        return x_scope * y_scope

    def top_side(self, radius):
        x_scope = Interval.open(self.x0+radius, self.x1-radius)
        y_scope = Interval.Ropen(self.y0, self.y0+radius)
        return x_scope * y_scope
 
    def bottom_side(self, radius):
        x_scope = Interval.open(self.x0+radius, self.x1-radius)
        y_scope = Interval.Lopen(self.y1-radius, self.y1)
        return x_scope * y_scope

    @property
    def aspect(self):
        return self.x_interval * self.y_interval

    def boundary(self, radius):
        x_scope = Interval(self.x0+radius, self.x1-radius)
        y_scope = Interval(self.y0+radius, self.y1-radius)
        return self.aspect - x_scope * y_scope