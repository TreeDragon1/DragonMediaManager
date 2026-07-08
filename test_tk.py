import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry("300x150")

label = tk.Label(root, text="Tkinter is working!")
label.pack(pady=30)

root.mainloop()
