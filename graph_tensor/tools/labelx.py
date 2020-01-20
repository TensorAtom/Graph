from tkinter import StringVar
from tkinter import Menu

from graph.drawing import Drawing


class Graph(Drawing):
    def __init__(self, master=None, cnf={}, selector=None, **kw):
        super().__init__(master, cnf, selector, **kw)
        self._create_variable()
        self.create_menu()
        self._reset_bind()

    def _reset_bind(self):
        self._draw_bind()
        self.current_id = None

    def _create_variable(self):
        '''菜单变量'''
        self.edit_var = StringVar()

    def create_menu(self):
        self.master.option_add('*tearOff', False)  # 设定菜单不能移除窗口
        menu_bar = Menu(self.master)  # 创建菜单栏
        self.master['menu'] = menu_bar  # 或者 root.config(menu=menubar)

        options = ('单个元素',
                   '全部的元素',
                   '全部的图元素',
                   '全部 ⬜',
                   '全部 ⚪',
                   '全部 ⯀',
                   '全部 ●',
                   '全部 ⸺'
                   )
        # 创建菜单
        edit_bar = Menu(menu_bar)
        move_menu = Menu(edit_bar)
        delete_menu = Menu(edit_bar)
        # 添加级联菜单
        menu_bar.add_cascade(label="编辑", menu=edit_bar)
        edit_bar.add_cascade(label="移动", menu=move_menu)
        edit_bar.add_cascade(label="删除", menu=delete_menu)
        kw_menu = {
            'variable': self.edit_var,
            'command': self.bind_graph
        }
        edit_bar.add_radiobutton(label=f"绘制", **kw_menu)
        [move_menu.add_radiobutton(
            label=f"移动{option}", **kw_menu) for option in options]
        [delete_menu.add_radiobutton(
            label=f"删除{option}", **kw_menu) for option in options]

    def select_graph(self, event):
        '''按压鼠标左键'''
        self.configure(cursor="target")
        self.update_xy(event)
        # 获取当前鼠标指示的对象的 id
        self.current_id = self.find_withtag('current')

    def move_strides(self, event):
        x, y = self.x, self.y
        self.update_xy(event)
        x_move = self.x - x
        y_move = self.y - y
        return x_move, y_move

    def move_graph(self, event, graph_id_or_tag):
        x_move, y_move = self.move_strides(event)
        self.move(graph_id_or_tag, x_move, y_move)

    def delete_graph(self, event, graph_id_or_tag):
        self.delete(graph_id_or_tag)

    def bind_graph(self):
        edit = self.edit_var.get()
        self.unbind('<ButtonRelease-1>')
        self.unbind('<1>')
        if edit == '绘制':
            self._reset_bind()
        elif '单个元素' in edit:
            self.bind('<1>', self.select_graph)
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, self.current_id)
            elif '删除' in edit:
                def action(event): return self.delete_graph(event, 'current')
            self.bind('<ButtonRelease-1>', action)
        elif '全部的元素' in edit:
            self.bind('<1>', self.select_graph)
            graph_id_or_tag = 'all'
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, graph_id_or_tag)
            elif '删除' in edit:
                def action(event): return self.delete_graph(
                    event, graph_id_or_tag)
            self.bind('<ButtonRelease-1>',  action)
        elif '全部的图元素' in edit:
            self.bind('<1>', self.select_graph)
            graph_id_or_tag = 'graph'
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, graph_id_or_tag)
            elif '删除' in edit:
                def action(event): return self.delete_graph(
                    event, graph_id_or_tag)
            self.bind('<ButtonRelease-1>',  action)
        elif '全部 ⬜' in edit:
            self.bind('<1>', self.select_graph)
            graph_id_or_tag = 'Rectangle'
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, graph_id_or_tag)
            elif '删除' in edit:
                def action(event): return self.delete_graph(
                    event, graph_id_or_tag)
            self.bind('<ButtonRelease-1>',  action)
        elif '全部 ⚪' in edit:
            self.bind('<1>', self.select_graph)
            graph_id_or_tag = 'Oval'
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, graph_id_or_tag)
            elif '删除' in edit:
                def action(event): return self.delete_graph(
                    event, graph_id_or_tag)
            self.bind('<ButtonRelease-1>',  action)
        elif '全部 ⸺' in edit:
            self.bind('<1>', self.select_graph)
            graph_id_or_tag = 'Line'
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, graph_id_or_tag)
            elif '删除' in edit:
                def action(event): return self.delete_graph(
                    event, graph_id_or_tag)
            self.bind('<ButtonRelease-1>',  action)
        elif '全部 ⯀' in edit:
            self.bind('<1>', self.select_graph)
            graph_id_or_tag = 'RectanglePoint'
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, graph_id_or_tag)
            elif '删除' in edit:
                def action(event): return self.delete_graph(
                    event, graph_id_or_tag)
            self.bind('<ButtonRelease-1>',  action)
        elif '全部 ●' in edit:
            self.bind('<1>', self.select_graph)
            graph_id_or_tag = 'OvalPoint'
            if '移动' in edit:
                def action(event): return self.move_graph(
                    event, graph_id_or_tag)
            elif '删除' in edit:
                def action(event): return self.delete_graph(
                    event, graph_id_or_tag)
            self.bind('<ButtonRelease-1>',  action)
