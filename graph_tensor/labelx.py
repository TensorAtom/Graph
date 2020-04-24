from tkinter import StringVar, ttk

from graph.atom import GraphScrollable
from graph.tk_utils import Window
from graph.creator import SelectorFrame
from pygui.tkinterx.meta import WindowMeta, showwarning, askokcancel, ask_window


class PopupLabel(WindowMeta):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

    def create_widget(self):
        self.add_row('Please enter the label: ', 'label')

    def run(self):
        self.withdraw()
        label = self.bunch['label'].get()
        if '' in [label]:
            showwarning(self)
        else:
            askokcancel(self, message='Do you want to confirm the submission?')


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
        bunch = ask_window(self, PopupLabel)
        return bunch['label'].get()

    def draw_label(self, event):
        graph_id = self.draw(event)
        if graph_id:
            label = self.set_label()
            self.bunch[graph_id] = label
            self.selector.info.set(self.bunch)


if __name__ == "__main__":
    root = Window()
    root.geometry('800x600')
    selector = SelectorFrame(root)
    graph = LabeledGraph(root, selector, background='lightgray')  # or GraphScrollable
    root.mainloop()
