import tkinter as tk
import tkinter.ttk as ttk


HEIGHT = 700
WIDTH = 1200

def prod_input_window(): # tu bedzie potrzebny parameter z czyms, gdzie beda magazynowane produkcje
    window = tk.Toplevel()
    window.title("Graph rewriting - production input")
    frame = tk.Frame(window, bg="#222", width=300, height=500)
    frame.pack(fill=tk.BOTH, expand=True)
    
    left_label = tk.Label(frame, text="Left side of the production", bg="#222", fg="#CCC", font="Courier")
    left_label.grid(row=0, column=0, pady=5)
    left_text_box = tk.Text(frame, width=50, height=10, bg="#CCC")
    left_text_box.insert(tk.INSERT, "Input left side of the production here\nin format specified in README")
    left_text_box.grid(row=1, column=0, padx=15, pady=10)

    right_label = tk.Label(frame, text="Right side of the production", bg="#222", fg="#CCC", font="Courier")
    right_label.grid(row=2, column=0, pady=5)
    right_text_box = tk.Text(frame, width=50, height=10, bg="#CCC")
    right_text_box.insert(tk.INSERT, "Input left side of the production here\nin format specified in README")
    right_text_box.grid(row=3, column=0, padx=10, pady=10)

    prod_label = tk.Label(frame, text="Transformation", bg="#222", fg="#CCC", font="Courier")
    prod_label.grid(row=4, column=0, pady=5)
    prod_text_box = tk.Text(frame, width=50, height=10, bg="#CCC")
    prod_text_box.insert(tk.INSERT, "Input production here in format\nspecified in README")
    prod_text_box.grid(row=5, column=0, padx=10, pady=10)

    s = ttk.Style()
    s.configure("my.TButton", font=("Courier", 12))
    button = ttk.Button(frame, width=15, text="Add production", style="my.TButton")
    button.grid(row=6, column=0, pady=10)


def graph_input_window(): # tu bedzie potrzebny parameter z czyms, gdzie beda magazynowane produkcje
    window = tk.Toplevel()
    window.title("Graph rewriting - graph input")
    frame = tk.Frame(window, bg="#222")
    frame.pack(fill=tk.BOTH, expand=True)

    prod_label = tk.Label(frame, text="Graph", bg="#222", fg="#CCC", font="Courier")
    prod_label.grid(row=4, column=0, pady=5)
    graph_text_box = tk.Text(frame, width=50, height=10, bg="#CCC")
    graph_text_box.insert(tk.INSERT, "Input your graph here in format\nspecified in README")
    graph_text_box.grid(row=5, column=0, padx=10, pady=10)

    s = ttk.Style()
    s.configure("my.TButton", font=("Courier", 12))
    button = ttk.Button(frame, width=15, text="Add graph", style="my.TButton")
    button.grid(row=6, column=0, pady=10)

def production_listing_frame(prod_list_frame):
    # TODO

    return

def show_graph(show_graph_frame):


    return


# MAIN WINDOW
def main():
    main_window = tk.Tk()
    main_window.title("Graph rewriting - main window")

    graph_frame = tk.Frame(main_window, height=HEIGHT, width=2*WIDTH/3)
    graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    graph_frame.propagate(0)

    prod_list_frame = tk.Frame(main_window, height=HEIGHT, width=WIDTH/3, bg="#555")
    prod_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    prod_list_frame.propagate(0)
    production_listing_frame(prod_list_frame) # TODO

    # BUTTONS TO OPEN NEW WINDOWS
    s = ttk.Style()
    s.configure("my.TButton", font=("Courier", 12))

    window_buttons = tk.Frame(graph_frame, height=40, bg="#222")
    window_buttons.pack(side=tk.TOP, fill=tk.X)
    window_buttons.propagate(0)

    graph_input_btn = ttk.Button(window_buttons, text="Graph input", width=20, command=graph_input_window, style="my.TButton")
    graph_input_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    prod_input_btn = ttk.Button(window_buttons, text="Production input", width=20, command=prod_input_window, style="my.TButton")
    prod_input_btn.pack(side=tk.RIGHT)

    # CHOOSE GRAPH TO SHOW AND APPLY PRODUCTION
    apply_frame = tk.Frame(graph_frame, height=80, bg="#222")
    apply_frame.pack(side=tk.BOTTOM, fill=tk.X)
    apply_frame.propagate(0)

    change_graph_frame = tk.Frame(apply_frame, bg="#222")
    change_graph_frame.pack(side=tk.LEFT)
    change_graph_frame.propagate(0)

    prod_label = tk.Label(change_graph_frame, text="Choose graph", bg="#222", fg="#CCC", font="Courier")
    prod_label.grid(row=0, column=0, columnspan=3, pady=5)
    
    change_left_button = ttk.Button(change_graph_frame, text="<", width=5, style="my.TButton" )
    change_left_button.grid(row=1, column=0, padx=5, pady=5)
    change_right_button = ttk.Button(change_graph_frame, text=">", width=5, style="my.TButton" )
    change_right_button.grid(row=1, column=1, padx=5, pady=5)

    apply_prod_frame = tk.Frame(apply_frame, bg="#222")
    apply_prod_frame.pack(side=tk.RIGHT)
    apply_prod_frame.propagate(0)

    prod_label = tk.Label(apply_prod_frame, text="Apply production", bg="#222", fg="#CCC", font="Courier")
    prod_label.grid(row=0, column=0, columnspan=3, pady=5)

    apply_button = ttk.Button(apply_prod_frame, text="Apply", width=5, style="my.TButton" )
    apply_button.grid(row=1, column=0, padx=5, pady=5) 

    entry_prod = tk.Entry(apply_prod_frame, bg="#CCC", width=5)
    entry_prod.grid(row=1, column=1, padx=5, pady=5)

    entry_graph = tk.Entry(apply_prod_frame, bg="#CCC", width=25)
    entry_graph.insert(tk.INSERT, "Graph indicies here")
    entry_graph.grid(row=1, column=2, padx=5, pady=5)


    # SHOW GRAPH
    show_graph_frame = tk.Frame(graph_frame, bg="#CCC")
    show_graph_frame.pack(side=tk.TOP, fill=tk.BOTH,  expand=True)
    show_graph(show_graph_frame) # TODO to raczej do zmiany, pod przycisk


    main_window.mainloop()


if __name__ == "__main__":
    main()