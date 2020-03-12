from tkinter import StringVar, Tk, filedialog
from PIL import Image, ImageTk

from graph.atom import Drawing


class Graph(Drawing):
    def __init__(self, root, home, selector, cnf={}, **kw):
        super().__init__(home, selector, cnf, **kw)
        self.root = root
        self.edit_var = StringVar()
        self.update_file_menu()
        self.update_edit_menu()

    def _reset_bind(self):
        self._draw_bind()
        self.selected_tags = None
        
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

    def update_file_menu(self):
        self.root.file_bar.add_radiobutton(label="Seek filename", command=self.load_image)

    def update_file(self):
        self.file_name = self.seek_filename()

    def update_image(self):
        self.I = self.name2image(self.file_name)

    def name2image(self, image_name):
        I = Image.open(image_name)
        image_file = ImageTk.PhotoImage(I)
        return ImageTk.PhotoImage(I)

    def load_image(self):
        self.update_file()
        self.update_image()
        self.reload_image()

    def reload_image(self):
        self.create_image(0, 0, anchor='nw', image=self.I, tags='image')

    def seek_folder_name(self):
        return filedialog.askdirectory()

    def seek_filename(self):
        return filedialog.askopenfilename()

    def seek_filenames(self):
        return filedialog.askopenfilenames()

    def update_edit_menu(self):
        kw_menu = {
                'variable': self.edit_var,
                'command': self.bind_graph
            }
        self.root.edit_bar.add_radiobutton(label=f"drawing", **kw_menu)
        [self.root.move_menu.add_radiobutton(
            label=f"move/{option}", **kw_menu) for option in self.tags_dict]
        [self.root.delete_menu.add_radiobutton(
            label=f"delete/{option}", **kw_menu) for option in self.tags_dict]

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

class LabeledGraphMeta(Graph):
    def __init__(self, root, home, selector, cnf={}, **kw):
        super().__init__(root, home, selector, cnf, **kw)

    def _init_params(self):
        self.x = self.y = 0
        self.file_name = None
        self.I = None

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
