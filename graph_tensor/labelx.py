from tkinter import Menu, StringVar, filedialog
from tkinter import Tk, ttk

from graph.creator import Selector
from graph.atom import Meta
from tools.label_helper import LabeledGraphMeta


class Window(Tk):
    def __init__(self):
        super().__init__()
        self._menu_init()
        self.create_menu()
    
    def _menu_init(self):
        # The settings menu cannot pop up from the window.
        self.option_add('*tearOff', False)

    def create_menu(self):
        self.menu_bar = Menu(self)
        self['menu'] = self.menu_bar  # Or `root.config(menu=menubar)`
        self._create_menu()
        
    def _create_menu(self):
        self._create_file_menu()
        self._create_edit_menu()
        
    def _create_edit_menu(self):
        self.edit_bar = Menu(self.menu_bar)
        self.move_menu = Menu(self.edit_bar)
        self.delete_menu = Menu(self.edit_bar)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_bar)
        self.edit_bar.add_cascade(label="move", menu=self.move_menu)
        self.edit_bar.add_cascade(label="delete", menu=self.delete_menu)

    def _create_file_menu(self):
        self.file_bar = Menu(self.menu_bar)
        self.image_menu = Menu(self.file_bar)
        self.tags_menu = Menu(self.file_bar)
        self.menu_bar.add_cascade(label="File", menu=self.file_bar)
        #file_bar.add_radiobutton(label="Ask folder name", command=self.seek_folder_name)
        #file_bar.add_radiobutton(label="Seek multiple filename", command=self.seek_filenames)


class LabeledGraph(Window):
    def __init__(self):
        super().__init__()
        self._home()
        self._set_scroll()
        self._create_canvas()
        self._scroll_command()
        self.layout()
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def _home(self):
        self.home = ttk.Frame()
        self.home['relief'] = 'groove'

    def _set_scroll(self):
        self.scroll_x = ttk.Scrollbar(self.home, orient='horizontal')
        self.scroll_y = ttk.Scrollbar(self.home, orient='vertical')

    def _create_canvas(self):
        self.pane = ttk.PanedWindow(self, orient = 'vertical')
        self.select_frame = ttk.LabelFrame(self.pane, text='Select', width=100, height=100)
        self.mark_frame = ttk.LabelFrame(self.pane, text='Marking', width=100, height=100)
        self.mark_button = ttk.Button(self.mark_frame, text='Load labels', command=self.load_label)
        self.label_notebook = ttk.Notebook(self.mark_frame)
        self.info_frame = ttk.LabelFrame(self.pane, text='Info', width=100, height=100)
        self.pane.add(self.select_frame)
        self.pane.add(self.info_frame)
        self.pane.add(self.mark_frame)
        self.icon_meta = Meta(self.select_frame , width=210, height=60, background='white')
        self.icon_creator = Selector(self.icon_meta)
        self.canvas = LabeledGraphMeta(self, self.home, self.icon_creator, background='lightgray')
        self.canvas.configure(width=800, height=600)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canvas.bind("<3>", self.mouse_motion)

    def create_table(self, frame, row, record):
        name, TYPE, table = record.split('|')
        select_type = 'ttk.Radiobutton' if TYPE == '0' else 'ttk.Checkbutton'
        table = table.split(',')
        ttk.Label(frame, text=name).grid(row=row, column=0)
        for k, s in enumerate(table):
            var = StringVar()
            eval(select_type)(frame, text=s, variable=var).grid(sticky='we', row=row, column=k+1)

    def load_label(self):
        label_file = filedialog.askopenfilename()
        with open(label_file, 'rb') as fp:
            teach = fp.read().decode()
        self.label_content = teach.split('## ')
        for records in self.label_content[1:]:
            records = records.strip().splitlines()
            frame = ttk.Frame(self.label_notebook)
            self.label_notebook.add(frame, text=records[0])
            for row, record in enumerate(records[4:]):
                self.create_table(frame, row, record)

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
        self.home.pack(side='left', expand='yes', fill='both')
        self.scroll_y.pack(side='right', fill='y')
        self.canvas.layout()
        self.pane.pack(side='right', fill='both')  
        self.mark_button.grid(row=0, column=0)
        self.label_notebook.grid(row=1, column=0)
        self.icon_meta.layout(0, 1)

    def resize(self, event):
        region = self.canvas.bbox('all')
        self.canvas.configure(scrollregion=region)


if __name__ == '__main__':
    root = LabeledGraph()
    root.title('Computer Vision')
    #test(root)
    root.mainloop()