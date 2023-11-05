import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class Ajudante():
    def __init__(self,debugging=False):
        self.root = tk.Tk()
        self.root.title("Image Copy Tool")
        self.root.geometry("400x400")
        self.root.eval('tk::PlaceWindow . center')

        self.base_de_dados_label = tk.Label(self.root, text="Base de Dados Folder:")
        self.base_de_dados_label.pack()
        self.base_de_dados_entry = tk.Entry(self.root)
        self.base_de_dados_entry.pack()
        self.base_de_dados_button = tk.Button(self.root, text="Browse", command=lambda: browse_folder(self.base_de_dados_entry))
        self.base_de_dados_button.pack()

        self.selecao_label = tk.Label(self.root, text="Selecao Folder:")
        self.selecao_label.pack()
        self.selecao_entry = tk.Entry(self.root)
        self.selecao_entry.pack()
        self.selecao_button = tk.Button(self.root, text="Browse", command=lambda: browse_folder(self.selecao_entry))
        self.selecao_button.pack()

        self.formato_quero_label = tk.Label(self.root, text="Formato Quero (Default: .ARW):")
        self.formato_quero_label.pack()
        self.formato_quero_entry = tk.Entry(self.root)
        self.formato_quero_entry.pack()

        self.formato_tenho_label = tk.Label(self.root, text="Formato Tenho (Default: .JPG):")
        self.formato_tenho_label.pack()
        self.formato_tenho_entry = tk.Entry(self.root)
        self.formato_tenho_entry.pack()

        self.start_button = tk.Button(self.root, text="Start Copying", command=self.start_copying)
        self.start_button.pack()

        self.progress_var_label = tk.Label(self.root, text="Progress bar")
        self.progress_var_label.pack()
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack()

        self.feedback_text = tk.StringVar()
        self.feedback_label = tk.Label(self.root, textvariable=self.feedback_text)
        self.feedback_label.pack()

        # if debugging: start_copying()
        self.copied_images = []
        self.copied_files= 0
        self.source_filepaths = []
        self.total_files = 0
        self.selection_images = []

        self.database = []
        self.wanted_files = []
        self.missing_images = []

        self.debugging = debugging

        # start GUI
        self.root.mainloop()

    def get_user_input(self):
        formato_quero = ".ARW"
        formato_tenho = ".JPG"
        if self.debugging:
            self.database = r"C:\Users\glauc\Desktop\testdir\DB"
            selecao =r"C:\Users\glauc\Desktop\testdir\sel"
        else:
            self.database = self.base_de_dados_entry.get()
            selecao = self.selecao_entry.get()
            formato_quero = self.formato_quero_entry.get()
            formato_tenho = self.formato_tenho_entry.get()
            if not formato_quero: formato_quero = ".ARW"
            if not formato_tenho: formato_tenho = ".JPG"

        self.dest_dir= os.path.join(selecao, "copiadas")

        if not os.path.exists(self.dest_dir): os.makedirs(self.dest_dir)
        self.wanted_files = [file.replace(formato_tenho, formato_quero) for path, subdir, files in os.walk(selecao) for
                             file in files]

    def start_copying(self):
        #global copied_images, copied_files, source_filepaths, missing_images, total_files, selection_images
        self.get_user_input()
        self.progress_var.set(0)

        self.copied_images       = set(os.listdir(self.dest_dir))
        self.selection_images    = set(self.wanted_files)
        self.total_files         = len(self.wanted_files)

        self.file_finder()

    def file_finder(self):
        self.copied_images = set(os.listdir(self.dest_dir))
        #global total_files, copied_files


        # TODO hardcode first pass giving as database an /ARW folder, then ignoring any /JPG and *sel

        for path, subdir, files in os.walk(self.database):
            for file in files:
                if file in self.wanted_files:
                    source_filepath = os.path.join(path, file)
                    self.file_copier(source_filepath)
                    self.root.update()

        if self.missing_images:
            self.feedback_text.set(f"Some images were not found in the base folder.\n"
                              f"Copied images: {self.copied_files}\n"
                              f"Missing files: {len(self.missing_images)}\n"
                              f"Failure rate: {100 * len(self.missing_images) / self.total_files}%")
        else:
            self.feedback_text.set(f"Copied {self.copied_files} of {self.total_files} images")

        if self.debugging: return
        # Show missing images and completion messages in the GUI
        self.messagebox.showinfo("Copying Complete", "Image copying process completed.\n"
                                                f"Copied {self.copied_files} of {self.total_files} images")
        if self.missing_images: self.messagebox.showinfo("Missing Images", str(self.missing_images))

        if self.missing_images:
            text = "Some images were not found in the base de dados.\n"
            text += f"Copied images: {(self.copied_files)}\n"
            text += f"Missing files: {len(self.missing_images)}\n"
            text += f"Fail rate: {100 * len(self.missing_images) / (self.total_files)}%\n"
            self.feedback_text.set(text)

        self.messagebox.showinfo("nao_encontradas", str(self.missing_images))

        self.messagebox.showinfo("Copying Complete", "Image copying process completed.")

    def file_copier(self, source_filepath):
        try:
            shutil.copy(source_filepath, self.dest_dir)
            self.copied_images.add(source_filepath)
            self.source_filepaths.append(source_filepath)
            self.copied_files += 1

            progress = int((self.copied_files / self.total_files) * 100)
            self.progress_var.set(progress)

            self.feedback_text.set(f"Copied {self.copied_files} of {self.total_files} images")
            self.root.update()

        except Exception as e:
            self.missing_images.append(source_filepath)
            self.feedback_text.set(self.feedback_text.get() + f"File {source_filepath} is wanted but could not be copied from {source_filepath} with error {e}.\n")
            print(e)


#



def browse_folder(entry):
   folder_path = filedialog.askdirectory()
   entry.delete(0, tk.END)
   entry.insert(0, folder_path)



ajudante = Ajudante(debugging=True)