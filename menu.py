import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from graph_utils import create_assembly_graph, plot_graph, draw_graph
from check import is_graph_connected, validate_entry
from create import create_random_matrix, read_matrix_from_file
def show_graphs():
    input_matrix = []
    try:
        for row in input_fields:
            input_matrix.append([float(entry.get()) for entry in row])
        input_matrix = np.array(input_matrix)
        show_graphs_with_matr(input_matrix)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите числовые значения.")
def show_graphs_with_matr(matr):
    # Преобразование матрицы в строку с отступами
    matrix_str = ""
    for row in matr:
        matrix_str += "\t".join(map(str, row)) + "\n"
    # Действия, которые необходимо выполнить после нажатия кнопки, например построение графа
    messagebox.showinfo("Информация", f"Матрица смежности:\n{matrix_str}")
    plt.figure(figsize=(12, 6))
    plt.title("Исходный граф")
    draw_graph(matr)
    plt.figure(figsize=(12, 6))
    plt.title("Преобразованный граф")
    transformed_graph = create_assembly_graph(matr)
    plot_graph(transformed_graph)
    reset_menu()
def input_matrix_layout(n):
    for widget in frame.winfo_children():
        widget.destroy()
    global input_fields
    input_fields = []
    vcmd = frame.register(validate_entry)
    for i in range(n):
        row_entries = []
        for j in range(n):
            entry = tk.Entry(frame, width=5, validate="key", validatecommand=(vcmd, '%P'))
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        input_fields.append(row_entries)
    build_button.config(state="normal")
    build_button.config(command=show_graphs)
def use_random_matrix():
    for widget in frame.winfo_children():
        widget.destroy()
    rand_matr = create_random_matrix()
    while not (is_graph_connected(rand_matr)):
        rand_matr = create_random_matrix()
    build_button.config(state="normal")
    build_button.config(command=lambda: show_graphs_with_matr(rand_matr))
def load_from_file():
    # global matrix_size, input_fields 
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    try:
        matrix = read_matrix_from_file(file_path)
        update_matrix_in_interface(matrix)
        build_button.config(state="normal")
        build_button.config(command=lambda: show_graphs_with_matr(matrix))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить матрицу: {e}")
def update_matrix_in_interface(matrix):
    # matrix_size: int = len(matrix)
    input_fields = []
    for widget in frame.winfo_children():
        widget.destroy()
    for i, row in enumerate(matrix):
        field_row = []
        for j, val in enumerate(row):
            entry = tk.Entry(frame, width=3)
            entry.grid(row=i, column=j)
            entry.insert(tk.END, val)
            field_row.append(entry)
        input_fields.append(field_row)
def set_manual_mode():
    for widget in frame.winfo_children():
        widget.destroy()
    size_label = tk.Label(frame, text="Размер матрицы смежности:")
    size_label.grid(row=0, column=0, padx=5, pady=5)
    size_entry = tk.Entry(frame)
    size_entry.grid(row=0, column=1, padx=5, pady=5)
    size_entry.bind("<Return>", lambda event: input_matrix_layout(int(size_entry.get())))
    build_button.config(state="disabled")
def reset_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    mode_label = tk.Label(frame, text="Выберите режим работы:")
    mode_label.pack(pady=5)
    manual_button = tk.Button(frame, text="Ввод матрицы вручную", command=set_manual_mode)
    manual_button.pack(pady=5)
    load_button = tk.Button(frame, text="Загрузить матрицу из файла", command=load_from_file)
    load_button.pack(pady=5)
    random_button = tk.Button(frame, text="Использовать случайную матрицу", command=use_random_matrix)
    random_button.pack(pady=5)
root = tk.Tk()
root.title("Графический интерфейс")
frame = tk.Frame(root)
frame.pack()
mode_label = tk.Label(frame, text="Выберите режим работы:")
mode_label.pack(pady=5)
manual_button = tk.Button(frame, text="Ввод матрицы вручную", command=set_manual_mode)
manual_button.pack(pady=5)
load_button = tk.Button(frame, text="Загрузить матрицу из файла", command=load_from_file)
load_button.pack(pady=5)
random_button = tk.Button(frame, text="Использовать случайную матрицу", command=use_random_matrix)
random_button.pack(pady=5)
build_button = tk.Button(root, text="Построить граф", state="disabled")
build_button.pack(pady=10)
root.mainloop()
