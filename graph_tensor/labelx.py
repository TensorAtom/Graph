from tkinter import Toplevel, StringVar, ttk

from graph.atom import GraphScrollable
from graph.tk_utils import Window
from graph.creator import SelectorFrame


class PopupLabel(Toplevel):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.label = StringVar()
        self.create_widget()

    def create_widget(self):
        self.tip_text = ttk.Label(self, text='Please enter the label: ')
        self.label_entry = ttk.Entry(self, textvariable=self.label)

    def layout(self):
        self.tip_text.grid(row=0, column=0, sticky='w')
        self.label_entry.grid(row=0, column=1, sticky='w')


class LabeledGraph(GraphScrollable):
    def __init__(self, master,  selector, cnf={}, **kw):
        super().__init__(master, selector, cnf, **kw)
        master.update_edit_menu(self)
        master.update_file_menu(self)
        # Makes the master widget change as the canvas size
        self.layout()
        selector.layout()
        selector.pack(side='right', fill='y')

    def set_label(self):
        popup = PopupLabel(self)
        popup.layout()
        self.wait_window(popup)
        return popup.label.get()

    def draw_label(self, event):
        graph_id = self.draw(event)
        if graph_id:
            label = self.set_label()
            self.bunch[graph_id] = label
            self.selector.info.set(self.bunch)

    def _draw_bind(self):
        self.bind("<1>", self.update_xy)
        self.bind("<ButtonRelease-1>", self.draw_label)

    def bind_graph(self):
        self.unbind('<ButtonRelease-1>')
        self.unbind('<1>')
        edit = self.edit_var.get()
        if edit == 'drawing':
            self._draw_bind()  # reset bind
        elif 'move' in edit:
            self.bind('<1>', lambda event: self.select_graph(
                event, edit.split('/')[1]))
            self.bind('<ButtonRelease-1>', self.move_graph)
        elif 'delete' in edit:
            self.bind('<1>', lambda event: self.select_graph(
                event, edit.split('/')[1]))
            self.bind('<ButtonRelease-1>', self.delete_graph)
        else:
            NotImplemented


if __name__ == "__main__":
    root = Window()
    root.geometry('800x600')
    selector = SelectorFrame(root)
    graph = LabeledGraph(root, selector, background='lightgray')  # or Graph
    root.mainloop()
