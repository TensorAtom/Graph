from sympy import Interval


class Rectangle(dict):
    def __init__(self, bbox, *args, **kw):
        super().__init__(*args, **kw)
        self.__dict__ = self
        self.x0, self.y0, self.x1, self.y1 = bbox
        self.scope_names = {'bottom_left_corner',
            'bottom_right_corner',
            'bottom_side',
            'left_side',
            'right_side',
            'top_left_corner',
            'top_right_corner',
            'top_side'}
    
    def get_scope(self, point, radius):
        for name in self.scope_names:
            scope_str = f"self.{name}"
            if point in  eval(scope_str)(radius):
                return name
        return 
    
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
