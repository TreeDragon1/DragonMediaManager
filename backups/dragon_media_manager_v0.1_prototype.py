import tkinter as tk
from tkinter import ttk
from pathlib import Path

MOVIE_ROOT = "/media/treedragon/Movies1"

class DragonMediaManager:

    def __init__(self, root):

        self.root = root
        self.root.title("Dragon Media Manager")
        self.root.geometry("900x650")

        title = tk.Label(
            root,
            text="🎬 Dragon Media Manager",
            font=("Arial",20,"bold")
        )
        title.pack(pady=10)

        info = tk.Label(
            root,
            text=f"Movie Library:\n{MOVIE_ROOT}",
            font=("Arial",11)
        )
        info.pack()

        self.output = tk.Text(root,height=25,width=100)
        self.output.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack()

        tk.Button(
            frame,
            text="Scan Library",
            width=20,
            command=self.scan_library
        ).grid(row=0,column=0,padx=5,pady=5)

        tk.Button(
            frame,
            text="Preview Changes",
            width=20,
            state="disabled"
        ).grid(row=0,column=1,padx=5,pady=5)

        tk.Button(
            frame,
            text="Organize Library",
            width=20,
            state="disabled"
        ).grid(row=0,column=2,padx=5,pady=5)

    def scan_library(self):

        self.output.delete("1.0",tk.END)

        root = Path(MOVIE_ROOT)

        movie_count = 0

        for folder in sorted(root.iterdir()):

            if not folder.is_dir():
                continue

            self.output.insert(
                tk.END,
                f"\n📂 {folder.name}\n"
            )

            for file in folder.iterdir():

                if file.suffix.lower() in (
                    ".mp4",
                    ".mkv",
                    ".avi",
                    ".mov"
                ):

                    movie_count += 1

                    self.output.insert(
                        tk.END,
                        f"   🎬 {file.name}\n"
                    )

        self.output.insert(
            tk.END,
            f"\n\nMovies Found: {movie_count}"
        )


root = tk.Tk()

DragonMediaManager(root)

root.mainloop()
