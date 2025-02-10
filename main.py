import tkinter as tk
from tkinter import messagebox
import lab_1  

def open_lab_window(lab_number):
    match lab_number:
        case 1:
            lab_1.open_lab() 
        case _:
            lab_window = tk.Toplevel(root)
            lab_window.title(f"Лабораторная {lab_number}")
            message_label = tk.Label(lab_window, text="Лабораторная в разработке", font=("Arial", 16))
            message_label.pack(pady=20)

def exit_program():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        root.quit()

root = tk.Tk()
root.title("Лабораторные работы")

title_label = tk.Label(root, text="Список лабораторных работ", font=("Arial", 16))
title_label.pack(pady=10)

for i in range(1, 8):
    lab_button = tk.Button(root, text=f"Лабораторная {i}", command=lambda i=i: open_lab_window(i))
    lab_button.pack(pady=5)

exit_button = tk.Button(root, text="Выход", command=exit_program)
exit_button.pack(pady=10)

root.mainloop()