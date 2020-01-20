from tkinter import StringVar
from tkinter import Menu

from graph.drawing import Drawing


class Graph(Drawing):
    def __init__(self, master=None, cnf={}, selector=None, **kw):
        super().__init__(master, cnf, selector, **kw)
        self._create_variable()
        self._menu_init()
        self.create_menu()
        self._reset_bind()

    def _reset_bind(self):
        self._draw_bind()
        self.selected_tags = None

    def _create_variable(self):
        self.edit_var = StringVar()

    @property
    def tags_dict(self):
        return {
            'Single element': 'current',
            'All elements': 'all',
            'All graphic elements': 'graph',
            '⬜': 'Rectangle',
            '⚪': 'Oval',
            '⸺': 'Line',
            '⯀': 'RectanglePoint',
            '●': 'OvalPoint'
        }

    def _create_edit_menu(self, menu_bar):
        edit_bar = Menu(menu_bar)
        move_menu = Menu(edit_bar)
        delete_menu = Menu(edit_bar)
        menu_bar.add_cascade(label="Edit", menu=edit_bar)
        edit_bar.add_cascade(label="move", menu=move_menu)
        edit_bar.add_cascade(label="delete", menu=delete_menu)
        kw_menu = {
            'variable': self.edit_var,
            'command': self.bind_graph
        }
        edit_bar.add_radiobutton(label=f"drawing", **kw_menu)
        [move_menu.add_radiobutton(
            label=f"move/{option}", **kw_menu) for option in self.tags_dict]
        [delete_menu.add_radiobutton(
            label=f"delete/{option}", **kw_menu) for option in self.tags_dict]

    def _menu_init(self):
        # The settings menu cannot pop up from the window.
        self.master.option_add('*tearOff', False)

    def create_menu(self):
        menu_bar = Menu(self.master)
        self.master['menu'] = menu_bar  # Or `root.config(menu=menubar)`
        self._create_edit_menu(menu_bar)

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
            self._reset_bind()
        elif 'move' in edit:
            self.bind('<1>', lambda event: self.select_graph(
                event, edit.split('/')[1]))
            self.bind('<ButtonRelease-1>', self.move_graph)
        elif 'delete' in edit:
            self.bind('<1>', lambda event: self.select_graph(
                event, edit.split('/')[1]))
            self.bind('<ButtonRelease-1>', self.delete_graph)
