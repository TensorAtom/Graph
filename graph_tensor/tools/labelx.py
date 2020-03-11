from tkinter import StringVar, ttk, Tk
from tkinter import Menu, filedialog
from PIL import Image, ImageTk

from graph.atom import Meta, Drawing
from graph.atom import 
from graph.creator import Selector


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


class LabeledGraphMeta(Graph):
    def __init__(self, master=None, cnf={}, selector=None, **kw):
        super().__init__(master, cnf, selector, **kw)

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

    def _create_file_menu(self, menu_bar):
        file_bar = Menu(menu_bar)
        image_menu = Menu(file_bar)
        tags_menu = Menu(file_bar)
        menu_bar.add_cascade(label="File", menu=file_bar)
        file_bar.add_radiobutton(
            label="Seek filename", command=self.load_image)
        #file_bar.add_radiobutton(label="Ask folder name", command=self.seek_folder_name)
        #file_bar.add_radiobutton(label="Seek multiple filename", command=self.seek_filenames)

    def seek_folder_name(self):
        return filedialog.askdirectory()

    def seek_filename(self):
        return filedialog.askopenfilename()

    def seek_filenames(self):
        return filedialog.askopenfilenames()

    def create_menu(self):
        menu_bar = Menu(self.master)
        self.master['menu'] = menu_bar  # Or `root.config(menu=menubar)`
        self._create_file_menu(menu_bar)
        self._create_edit_menu(menu_bar)

    def name2image(self, image_name):
        I = Image.open(image_name)
        image_file = ImageTk.PhotoImage(I)
        return ImageTk.PhotoImage(I)

    def update_file(self):
        self.file_name = self.seek_filename()

    def update_image(self):
        self.I = self.name2image(self.file_name)

    def load_image(self):
        self.update_file()
        self.update_image()
        self.reload_image()

    def reload_image(self):
        self.create_image(0, 0, anchor='nw', image=self.I, tags='image')

    
class LabeledGraph(Tk):
    def __init__(self):
        super().__init__()
        self._set_scroll()
        self._create_canvas()
        self._scroll_command()
        #self.frame = ttk.Frame(self.canvas)
        #self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.layout()
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def _set_scroll(self):
        self.scroll_x = ttk.Scrollbar(orient='horizontal')
        self.scroll_y = ttk.Scrollbar(orient='vertical')

    def _create_canvas(self):
        self.icon_meta = Meta(self, width=210, height=60)
        self.icon_creator = Selector(self.icon_meta)
        self.canvas = LabeledGraphMeta(self, selector=self.icon_creator, background='white')
        self.canvas.configure(width=800, height=600)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

    def _scroll_command(self):
        self.scroll_x['command'] = self.canvas.xview
        self.scroll_y['command'] = self.canvas.yview

    def layout(self):
        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.scroll_x.grid(row=1, column=0, sticky="we")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.icon_meta.layout(0, 2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def resize(self, event):
        region = self.canvas.bbox('all')
        self.canvas.configure(scrollregion=region)
