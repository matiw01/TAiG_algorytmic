import tkinter as tk
import tkinter.ttk as ttk


HEIGHT = 700
WIDTH = 1200

def prod_input_window(): # tu bedzie potrzebny parameter z czyms, gdzie beda magazynowane produkcje
    window = tk.Toplevel()
    window.title("Graph rewriting - production input")
    frame = tk.Frame(window, bg="black", width=300, height=500)
    frame.pack(fill=tk.BOTH, expand=True)
    
    left_label = tk.Label(frame, text="Left side of the production", bg="black", fg="white")
    left_label.grid(row=0, column=0, pady=5)
    left_text_box = tk.Text(frame, width=50, height=10)
    left_text_box.grid(row=1, column=0, padx=15, pady=15)

    right_label = tk.Label(frame, text="Right side of the production", bg="black", fg="white")
    right_label.grid(row=2, column=0)
    right_text_box = tk.Text(frame, width=50, height=10)
    right_text_box.grid(row=3, column=0, padx=10, pady=15)

    prod_label = tk.Label(frame, text="Transformation", bg="black", fg="white")
    prod_label.grid(row=4, column=0)
    prod_text_box = tk.Text(frame, width=50, height=10)
    prod_text_box.grid(row=5, column=0, padx=10, pady=15)

    button = tk.Button(frame, width=15, height=2, text="Add production")
    button.grid(row=6, column=0, pady=5)


def graph_input_window():
    window = tk.Toplevel()
    window.title("Graph rewriting - graph input")
    frame = tk.Frame(window, bg="black")
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text="Graph", bg="black", fg="white")
    label.grid(row=4, column=0, pady=5)
    text_box = tk.Text(frame, width=50, height=10)
    text_box.grid(row=5, column=0, padx=10, pady=15)

    button = tk.Button(frame, width=15, height=2, text="Add graph")
    button.grid(row=6, column=0, pady=5)

main_window = tk.Tk()
main_window.title("Graph rewriting - main window")

graph_frame = tk.Frame(main_window, height=HEIGHT, width=2*WIDTH/3, bg="red")
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
graph_frame.propagate(0)

prod_list_frame = tk.Frame(main_window, height=HEIGHT, width=WIDTH/3, bg="blue")
prod_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
prod_list_frame.propagate(0)

# BUTTONS TO OPEN NEW WINDOWS
window_buttons = tk.Frame(graph_frame, height=40, bg="yellow")
window_buttons.pack(side=tk.TOP, fill=tk.X)
window_buttons.propagate(0)

graph_input_btn = ttk.Button(window_buttons, text="Graph input", width=20, command=graph_input_window)
graph_input_btn.pack(side=tk.RIGHT, padx=5, pady=5)

prod_input_btn = ttk.Button(window_buttons, text="Production input", width=20, command=prod_input_window)
prod_input_btn.pack(side=tk.RIGHT)

# CHOOSE GRAPH TO SHOW AND APPLY PRODUCTION
apply_frame = tk.Frame(graph_frame, height=50, bg="green")
apply_frame.pack(side=tk.BOTTOM, fill=tk.X)

# SHOW GRAPH
show_graph_frame = tk.Frame(graph_frame, bg="black")
show_graph_frame.pack(side=tk.TOP, fill=tk.BOTH,  expand=True)





main_window.mainloop()