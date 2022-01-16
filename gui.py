import tkinter as tk
import tkinter.ttk as ttk

from PIL import ImageTk

from main import Main

DEFAULT_GRAPH_INPUT_STRING = "1, a; 2, x; 3, N; 4, asvae;\n1, 3, s; 1, 4, M; 2, 2, ab; 4, 2, :D; 2, 3, cds;"

HEIGHT = 700
WIDTH = 1200

BG_COLOR = "#222222"
FG_COLOR = "#CCCCCC"
PROD_BG_COLOR = "#777777"
FONT = "Courier"


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

        # window = tk.Toplevel()
        # window.title("Production added")
        # frame = tk.Frame(window, bg=BG_COLOR, width=300, height=100)
        # frame.pack(fill=tk.BOTH, expand=True)
        # frame.propagate(0)
        # label = tk.Label(frame, text="Production added", bg=BG_COLOR, fg=FG_COLOR, font=(FONT, 18))
        # label.pack(fill=tk.BOTH, expand=True)

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

        # window = tk.Toplevel()
        # window.title("Graph added")
        # frame = tk.Frame(window, bg=BG_COLOR, width=300, height=100)
        # frame.pack(fill=tk.BOTH, expand=True)
        # frame.propagate(0)
        # label = tk.Label(frame, text="Graph added", bg=BG_COLOR, fg=FG_COLOR, font=(FONT, 18))
        # label.pack(fill=tk.BOTH, expand=True)

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
    img = ImageTk.PhotoImage(data=graph_data)

    for widget in show_graph_frame.winfo_children():
        widget.destroy()

    label = tk.Label(show_graph_frame, image=img, bg=FG_COLOR)
    label.photo = img
    label.pack(fill=tk.BOTH, expand=True)


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
    prod_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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
    entry_prod.grid(row=1, column=1, padx=5, pady=5)

    entry_graph = tk.Entry(apply_prod_frame, bg=FG_COLOR, width=25)
    entry_graph.insert(tk.INSERT, "Graph indicies here")
    entry_graph.grid(row=1, column=2, padx=5, pady=5)

    main_window.mainloop()


if __name__ == "__main__":
    main()
