from collections import namedtuple
import random
import io
import tkinter as tk
import tkinter.ttk as ttk
from unicodedata import name

from PIL import ImageTk, Image

from main import Main

DEFAULT_GRAPH_INPUT_STRING = "1, A; 2, B; 3, C; 4, D;\n1, 3, s; 1, 4, xd; 2, 2, a; 4, 2, r; 2, 3, d;"

HEIGHT = 700
WIDTH = 1200

BG_COLOR = "#222222"
FG_COLOR = "#CCCCCC"
PROD_BG_COLOR = "#777777"
FONT = "Courier"

#########################################################
# code for zooming and scrolling in on graph
# stolen from https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan

class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class Zoom_Advanced(ttk.Frame):
    ''' Advanced zoom of the image '''
    def __init__(self, mainframe, image_data):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set, bg=FG_COLOR)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        self.image = Image.open(io.BytesIO(image_data))  # open image
        self.width, self.height = self.image.size
        self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.3  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        # centering the image inside of canvas
        Center_coords = namedtuple("center_coords", "x y")
        center = Center_coords(int((0.5*mainframe.winfo_width())-(0.5*self.width)), int((0.5*mainframe.winfo_height())-(0.5*self.height)))
        self.move_to(center)

        self.show_image()

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self, event=None):
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

########################################################


def prod_input_window(backend, prod_frame):
    window = tk.Toplevel()
    window.title("Graph rewriting - production input")
    frame = tk.Frame(window, bg=BG_COLOR, width=300, height=500)
    frame.pack(fill=tk.BOTH, expand=True)

    left_label = tk.Label(frame, text="Left side of the production", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    left_label.grid(row=0, column=0, pady=5)
    left_text_box = tk.Text(frame, width=80, height=6, bg=FG_COLOR)
    left_text_box.insert(tk.INSERT, "1, A;")
    left_text_box.grid(row=1, column=0, padx=15, pady=10)

    right_label = tk.Label(frame, text="Right side of the production", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    right_label.grid(row=2, column=0, pady=5)
    right_text_box = tk.Text(frame, width=80, height=6, bg=FG_COLOR)
    right_text_box.insert(tk.INSERT, "1, A; 2, M;\n1, 2, am;")
    right_text_box.grid(row=3, column=0, padx=10, pady=10)

    prod_label = tk.Label(frame, text="Transformation", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    prod_label.grid(row=4, column=0, pady=5)
    prod_text_box = tk.Text(frame, width=80, height=10, bg=FG_COLOR)
    prod_text_box.insert(tk.INSERT, "s, out, 1; A, N, s, out; M, N, -a, in;\nai, out, 1; A, I, ai, out; M, I, -c, in;")
    prod_text_box.grid(row=5, column=0, padx=10, pady=10)

    def add_prod(prod_frame):
        # validation
        left = left_text_box.get("1.0", 'end-1c')
        right = right_text_box.get("1.0", 'end-1c')
        prod = prod_text_box.get("1.0", 'end-1c')
        backend.add_production(left, "left", right, "right", prod)

        l_graph, r_graph = backend.productions[-1].get_lr_graphs()
        add_production_to_list(prod_frame, l_graph, r_graph, prod, len(backend.productions) - 1)

    s = ttk.Style()
    s.configure("my.TButton", font=(FONT, 12))
    button = ttk.Button(frame, width=15, text="Add production", style="my.TButton",
                        command=lambda: add_prod(prod_frame))
    button.grid(row=6, column=0, pady=10)


def graph_input_window(backend):
    window = tk.Toplevel()
    window.title("Graph rewriting - graph input")
    frame = tk.Frame(window, bg=BG_COLOR)
    frame.pack(fill=tk.BOTH, expand=True)

    prod_label = tk.Label(frame, text="Graph", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    prod_label.grid(row=1, column=0, pady=5)
    graph_text_box = tk.Text(frame, width=80, height=6, bg=FG_COLOR)
    graph_text_box.insert(tk.INSERT, DEFAULT_GRAPH_INPUT_STRING)
    graph_text_box.grid(row=2, column=0, padx=10, pady=10)

    def add_graph():
        # validation
        graph = graph_text_box.get("1.0", 'end-1c')
        backend.add_graph(graph, "graph")

    s = ttk.Style()
    s.configure("my.TButton", font=(FONT, 12))
    button = ttk.Button(frame, width=15, text="Add graph", style="my.TButton", command=add_graph)
    button.grid(row=6, column=0, pady=10)


def add_production_to_list(prod_frame, l_graph, r_graph, prod, num):
    frame = tk.Frame(prod_frame, bg=PROD_BG_COLOR)

    num_label = tk.Label(frame, text=f"{num}", font=(FONT, 20), bg=PROD_BG_COLOR)
    num_label.grid(row=0, column=0, rowspan=2)

    l_graph_img = ImageTk.PhotoImage(data=l_graph.get_graph(PROD_BG_COLOR))
    l_graph_label = tk.Label(frame, image=l_graph_img, bg=PROD_BG_COLOR)
    l_graph_label.photo = l_graph_img
    l_graph_label.grid(row=0, column=1)

    arrow_label = tk.Label(frame, text="=>", font=(FONT, 10), bg=PROD_BG_COLOR)
    arrow_label.grid(row=0, column=2)

    r_graph_img = ImageTk.PhotoImage(data=r_graph.get_graph(PROD_BG_COLOR))
    r_graph_img.photo = r_graph_img
    r_graph_label = tk.Label(frame, image=r_graph_img, bg=PROD_BG_COLOR)
    r_graph_label.photo = r_graph_img
    r_graph_label.grid(row=0, column=3)

    prod_label = tk.Label(frame, text=prod, bg=PROD_BG_COLOR, font=(FONT, 8))
    prod_label.grid(row=1, column=1, columnspan=3)

    frame.pack(side=tk.TOP, pady=5)


def show_graph(show_graph_frame, backend, number):
    global current_graph
    current_graph = number

    if number < len(backend.graphs):
        graph = backend.graphs[number]
        current_graph = number
    else:
        return

    graph_data = graph.get_graph(FG_COLOR)

    for widget in show_graph_frame.winfo_children():
        widget.destroy()

    app = Zoom_Advanced(show_graph_frame, image_data=graph_data)


def apply_production(show_graph_frame, backend, prod_num, verticies):
    global current_graph
    graph = backend.graphs[current_graph]

    if prod_num < len(backend.productions):
        production = backend.productions[prod_num]
    else:
        return

    backend.use_production(production, graph, verticies, current_graph)
    show_graph(show_graph_frame, backend, current_graph)


# MAIN WINDOW
current_graph = 0


def basics(M, prod_frame):
    A1 = """s, out, 1; A, N, s, out; N, N, -n, in; N, N, n, in;"""
    A2 = """s, out, 1; A, N, s, out; M, N, -a, in;
ai, out, 1; A, I, ai, out; M, I, -c, in;"""
    A3 = """am, out, 1; A, M, am, out; E, M, -b, in;"""
    A4 = """ae, out, 1; A, E, ae, out; I, E, -l, in;
am, out, 1; A, M, am, out; I, M, c, in;"""

    g_l1 = """1, A;"""
    g_r1 = """1, A; 2, N;
1, 2, s;"""
    g_l2 = """1, A;"""
    g_r2 = """1, A; 2, M;
1, 2, am;"""
    g_l3 = """1, A;"""
    g_r3 = """1, A; 2, E;
1, 2, ae;"""
    g_l4 = """1, A;"""
    g_r4 = """1, A; 2, I;
1, 2, ai;"""
    grafs = [(g_l1, "g_l1", g_r1, "g_r1"),
             (g_l2, "g_l2", g_r2, "g_r2"),
             (g_l3, "g_l3", g_r3, "g_r3"),
             (g_l4, "g_l4", g_r4, "g_r4"),
             ]
    osadzenia = [A1, A2, A3, A4]
    for i in range(len(grafs)):
        for j in range(2):
            M.add_graph(grafs[i][j * 2], grafs[i][j * 2 + 1])
    for i in range(len(grafs)):
        M.add_production(grafs[i][0], grafs[i][1], grafs[i][2], grafs[i][3], osadzenia[i])
        add_production_to_list(prod_frame, M.graphs[i * 2], M.graphs[i * 2 + 1], osadzenia[i], i)


def main():
    # API FOR BACKEND
    backend = Main()

    main_window = tk.Tk()
    main_window.title("Graph rewriting - main window")

    # LISTING PRODUCTIONS

    prod_list_frame = tk.Frame(main_window, height=HEIGHT, width=WIDTH / 3, bg=PROD_BG_COLOR)
    prod_list_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    # prod_list_frame.propagate(0)

    prod_canvas = tk.Canvas(prod_list_frame, bg=PROD_BG_COLOR, bd=0, highlightthickness=0, relief='ridge')
    prod_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(prod_list_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar.config(command=prod_canvas.yview)
    prod_canvas.config(yscrollcommand=scrollbar.set)
    prod_canvas.bind("<Configure>", lambda e: prod_canvas.configure(scrollregion=prod_canvas.bbox("all")))

    prod_frame = tk.Frame(prod_canvas, bg=PROD_BG_COLOR)
    prod_frame.pack()
    basics(backend, prod_frame)

    prod_canvas.create_window((0, 0), window=prod_frame, anchor="nw")

    # SIDE WITH THE GRAPH

    graph_frame = tk.Frame(main_window, height=HEIGHT, width=2 * WIDTH / 3, bg=FG_COLOR)
    graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    graph_frame.propagate(False)

    # BUTTONS TO OPEN NEW WINDOWS
    s = ttk.Style()
    s.configure("my.TButton", font=(FONT, 12))

    window_buttons = tk.Frame(graph_frame, height=40, bg=BG_COLOR)
    window_buttons.pack(side=tk.TOP, fill=tk.X)
    window_buttons.propagate(False)

    graph_input_btn = ttk.Button(window_buttons, text="Graph input", width=20,
                                 command=lambda: graph_input_window(backend), style="my.TButton")
    graph_input_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    prod_input_btn = ttk.Button(window_buttons, text="Production input", width=20,
                                command=lambda: prod_input_window(backend, prod_frame), style="my.TButton")
    prod_input_btn.pack(side=tk.RIGHT)

    # SHOW GRAPH FRAME
    show_graph_frame = tk.Frame(graph_frame, bg=FG_COLOR)
    show_graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # CHOOSE GRAPH TO SHOW AND APPLY PRODUCTION
    apply_frame = tk.Frame(graph_frame, height=80, bg=BG_COLOR)
    apply_frame.pack(side=tk.BOTTOM, fill=tk.X)
    apply_frame.propagate(False)

    # CHANGE SHOWN GRAPH
    change_graph_frame = tk.Frame(apply_frame, bg=BG_COLOR)
    change_graph_frame.pack(side=tk.LEFT)
    change_graph_frame.propagate(False)

    prod_label = tk.Label(change_graph_frame, text="Choose graph", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    prod_label.grid(row=0, column=0, columnspan=3, pady=5)

    change_button = ttk.Button(change_graph_frame, text="Change to", width=10, style="my.TButton",
                               command=lambda: show_graph(show_graph_frame, backend, int(change_entry.get())))
    change_button.grid(row=1, column=0, padx=5, pady=5)
    change_entry = tk.Entry(change_graph_frame, bg=FG_COLOR, width=5)
    change_entry.insert(tk.INSERT, "0")
    change_entry.grid(row=1, column=1, padx=5, pady=5)

    # REVERSE GRAPH
    def show_previous_graph():
        global current_graph
        backend.graphs[current_graph] = backend.prev_graphs[current_graph]
        show_graph(show_graph_frame, backend, current_graph)

    reverse_frame = tk.Frame(apply_frame, bg=BG_COLOR)
    reverse_frame.pack(side=tk.LEFT, padx=20)

    reverse_label = tk.Label(reverse_frame, text="Reverse graph to previous state", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    reverse_label.grid(row=0, column=0, pady=5)
    reverse_button = ttk.Button(reverse_frame, text="Reverse", width=10, style="my.TButton",
                                command=show_previous_graph)
    reverse_button.grid(row=1, column=0, pady=5)

    # APPLY PRODUCTION
    apply_prod_frame = tk.Frame(apply_frame, bg=BG_COLOR)
    apply_prod_frame.pack(side=tk.RIGHT)
    apply_prod_frame.propagate(False)

    prod_label = tk.Label(apply_prod_frame, text="Apply production", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    prod_label.grid(row=0, column=0, columnspan=3, pady=5)

    apply_button = ttk.Button(apply_prod_frame, text="Apply", width=5, style="my.TButton",
                              command=lambda: apply_production(show_graph_frame, backend, int(entry_prod.get()),
                                                               [int(x) for x in entry_graph.get().split(" ")]))
    apply_button.grid(row=1, column=0, padx=5, pady=5)

    entry_prod = tk.Entry(apply_prod_frame, bg=FG_COLOR, width=5)
    entry_prod.insert(tk.INSERT, "0")
    entry_prod.grid(row=1, column=1, padx=5, pady=5)

    entry_graph = tk.Entry(apply_prod_frame, bg=FG_COLOR, width=25)
    entry_graph.insert(tk.INSERT, "1 1")
    entry_graph.grid(row=1, column=2, padx=5, pady=5)

    main_window.mainloop()


if __name__ == "__main__":
    main()
