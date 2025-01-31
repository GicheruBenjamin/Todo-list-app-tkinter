import tkinter as tk
from tkinter import messagebox

def add_task():
    task = task_entry.get()
    if task != "":
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(selected_task_index)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove!")

def clear_tasks():
    tasks_listbox.delete(0, tk.END)

def mark_completed():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = tasks_listbox.get(selected_task_index)
        tasks_listbox.delete(selected_task_index)
        tasks_listbox.insert(tk.END, f"✔ {task}")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as completed!")

# GUI setup
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x400")

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

tasks_listbox = tk.Listbox(root, width=50, height=15)
tasks_listbox.pack()

button_frame = tk.Frame(root)
button_frame.pack()

add_button = tk.Button(button_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=0, padx=5, pady=5)

remove_button = tk.Button(button_frame, text="Remove Task", command=remove_task)
remove_button.grid(row=0, column=1, padx=5, pady=5)

complete_button = tk.Button(button_frame, text="Mark Completed", command=mark_completed)
complete_button.grid(row=0, column=2, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_tasks)
clear_button.grid(row=0, column=3, padx=5, pady=5)

root.mainloop()
