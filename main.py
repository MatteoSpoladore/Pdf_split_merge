import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pypdf import PdfReader, PdfWriter

# Impostazioni generali del tema
ctk.set_appearance_mode("System")  # Modalità System, Dark o Light
ctk.set_default_color_theme("blue")  # Tema dei bottoni


class PdfManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF Manager: Separa & Unisci")
        self.geometry("800x600")
        self.minsize(600, 450)

        # Configurazione griglia principale
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Dizionario per memorizzare le schermate (Frame)
        self.frames = {}

        # Inizializzazione delle schermate
        for F in (HomeFrame, SplitFrame, MergeFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            # Sovrappone i frame nella stessa cella di griglia
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostra la schermata iniziale
        self.show_frame("HomeFrame")

    def show_frame(self, page_name):
        """Porta in primo piano il frame richiesto"""
        frame = self.frames[page_name]
        frame.tkraise()


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sezione Sinistra: SEPARA
        self.frame_split = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_split.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_split.grid_rowconfigure(0, weight=1)
        self.frame_split.grid_columnconfigure(0, weight=1)

        self.btn_go_split = ctk.CTkButton(
            self.frame_split,
            text="SEPARA PDF",
            font=ctk.CTkFont(size=24, weight="bold"),
            command=lambda: controller.show_frame("SplitFrame"),
        )
        self.btn_go_split.grid(row=0, column=0, sticky="nsew")

        # Sezione Destra: UNISCI
        self.frame_merge = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_merge.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.frame_merge.grid_rowconfigure(0, weight=1)
        self.frame_merge.grid_columnconfigure(0, weight=1)

        self.btn_go_merge = ctk.CTkButton(
            self.frame_merge,
            text="UNISCI PDF",
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#2FA572",
            hover_color="#106A43",
            command=lambda: controller.show_frame("MergeFrame"),
        )
        self.btn_go_merge.grid(row=0, column=0, sticky="nsew")


class SplitFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pdf_path = None

        # Pulsante Indietro
        self.btn_back = ctk.CTkButton(
            self,
            text="< Indietro",
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=20)

        self.lbl_title = ctk.CTkLabel(
            self, text="Separa PDF", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_title.pack(pady=(0, 20))

        # Selezione File
        self.btn_select = ctk.CTkButton(
            self, text="Seleziona File PDF", command=self.select_pdf
        )
        self.btn_select.pack(pady=10)

        self.lbl_file = ctk.CTkLabel(self, text="Nessun file selezionato")
        self.lbl_file.pack(pady=5)

        # Opzioni di Separazione
        self.radio_var = tk.IntVar(value=0)

        self.radio_single = ctk.CTkRadioButton(
            self,
            text="Estrai ogni singola pagina",
            variable=self.radio_var,
            value=0,
            command=self.toggle_entry,
        )
        self.radio_single.pack(pady=10)

        self.radio_range = ctk.CTkRadioButton(
            self,
            text="Estrai per intervalli (es. 2-3, 4-7)",
            variable=self.radio_var,
            value=1,
            command=self.toggle_entry,
        )
        self.radio_range.pack(pady=10)

        self.entry_ranges = ctk.CTkEntry(
            self, placeholder_text="Es. 1, 3, 5-8", state="disabled", width=300
        )
        self.entry_ranges.pack(pady=5)

        # Esecuzione
        self.btn_execute = ctk.CTkButton(
            self,
            text="Esegui Separazione",
            command=self.split_pdf,
            fg_color="#C85000",
            hover_color="#8F3900",
        )
        self.btn_execute.pack(pady=30)

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.pdf_path = path
            self.lbl_file.configure(text=os.path.basename(path))

    def toggle_entry(self):
        if self.radio_var.get() == 1:
            self.entry_ranges.configure(state="normal")
        else:
            self.entry_ranges.configure(state="disabled")

    def parse_intervals(self, text, max_pages):
        """Converte la stringa stile Word (es. 2-3, 5) in una lista di liste di pagine 0-indexed."""
        chunks = []
        parts = text.split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue

            pages_in_chunk = []
            if "-" in part:
                try:
                    start, end = part.split("-")
                    start_idx = int(start.strip()) - 1
                    end_idx = int(end.strip()) - 1
                    for i in range(start_idx, end_idx + 1):
                        if 0 <= i < max_pages:
                            pages_in_chunk.append(i)
                except ValueError:
                    pass
            else:
                try:
                    idx = int(part) - 1
                    if 0 <= idx < max_pages:
                        pages_in_chunk.append(idx)
                except ValueError:
                    pass

            if pages_in_chunk:
                chunks.append(pages_in_chunk)
        return chunks

    def split_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning("Attenzione", "Seleziona prima un file PDF.")
            return

        out_dir = filedialog.askdirectory(title="Seleziona cartella di destinazione")
        if not out_dir:
            return

        try:
            reader = PdfReader(self.pdf_path)
            total_pages = len(reader.pages)
            base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]

            mode = self.radio_var.get()

            if mode == 0:  # Ogni singola pagina
                for i in range(total_pages):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    out_path = os.path.join(out_dir, f"{base_name}_pag_{i+1}.pdf")
                    with open(out_path, "wb") as f:
                        writer.write(f)
            else:  # Intervalli
                intervals_text = self.entry_ranges.get()
                chunks = self.parse_intervals(intervals_text, total_pages)

                if not chunks:
                    messagebox.showerror(
                        "Errore", "Formato intervalli non valido o pagine fuori range."
                    )
                    return

                for idx, chunk in enumerate(chunks):
                    writer = PdfWriter()
                    for p in chunk:
                        writer.add_page(reader.pages[p])

                    out_path = os.path.join(out_dir, f"{base_name}_parte_{idx+1}.pdf")
                    with open(out_path, "wb") as f:
                        writer.write(f)

            messagebox.showinfo("Successo", "PDF separato con successo!")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore:\n{str(e)}")


class MergeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.btn_back = ctk.CTkButton(
            self,
            text="< Indietro",
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=20)

        self.lbl_title = ctk.CTkLabel(
            self, text="Unisci PDF", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_title.pack(pady=(0, 10))

        # Controlli Superiori
        self.frame_controls = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controls.pack(pady=10)

        self.btn_add = ctk.CTkButton(
            self.frame_controls, text="Aggiungi PDF", command=self.add_pdfs
        )
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_remove = ctk.CTkButton(
            self.frame_controls,
            text="Rimuovi Selezionato",
            command=self.remove_pdf,
            fg_color="#D13A3A",
            hover_color="#8F2525",
        )
        self.btn_remove.grid(row=0, column=1, padx=5)

        # Listbox per ordinamento (Tkinter standard integrato per via della semplicità di riordino)
        self.listbox_frame = ctk.CTkFrame(self)
        self.listbox_frame.pack(pady=10, fill="both", expand=True, padx=50)

        self.listbox = tk.Listbox(
            self.listbox_frame,
            selectmode=tk.SINGLE,
            font=("Arial", 12),
            bg="#2B2B2B",
            fg="white",
            selectbackground="#1F538D",
        )
        self.listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Bottoni di Ordinamento a lato della listbox
        self.frame_order = ctk.CTkFrame(self.listbox_frame, fg_color="transparent")
        self.frame_order.pack(side="right", fill="y", padx=10, pady=10)

        self.btn_up = ctk.CTkButton(
            self.frame_order, text="Su ▲", width=60, command=self.move_up
        )
        self.btn_up.pack(pady=5)

        self.btn_down = ctk.CTkButton(
            self.frame_order, text="Giù ▼", width=60, command=self.move_down
        )
        self.btn_down.pack(pady=5)

        # Bottone Unione
        self.btn_merge = ctk.CTkButton(
            self,
            text="Conferma & Unisci",
            command=self.merge_pdfs,
            fg_color="#2FA572",
            hover_color="#106A43",
        )
        self.btn_merge.pack(pady=20)

        self.pdf_list = []  # Mantiene traccia dei percorsi assoluti

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for f in files:
            self.pdf_list.append(f)
            self.listbox.insert(tk.END, os.path.basename(f))

    def remove_pdf(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        self.listbox.delete(idx)
        self.pdf_list.pop(idx)

    def move_up(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx == 0:
            return

        # Scambia nella UI
        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx - 1, text)
        self.listbox.selection_set(idx - 1)

        # Scambia nella lista
        self.pdf_list[idx], self.pdf_list[idx - 1] = (
            self.pdf_list[idx - 1],
            self.pdf_list[idx],
        )

    def move_down(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx == self.listbox.size() - 1:
            return

        # Scambia nella UI
        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx + 1, text)
        self.listbox.selection_set(idx + 1)

        # Scambia nella lista
        self.pdf_list[idx], self.pdf_list[idx + 1] = (
            self.pdf_list[idx + 1],
            self.pdf_list[idx],
        )

    def merge_pdfs(self):
        if len(self.pdf_list) < 2:
            messagebox.showwarning(
                "Attenzione", "Aggiungi almeno due file PDF da unire."
            )
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salva PDF Unito Come",
        )
        if not out_path:
            return

        try:
            writer = PdfWriter()
            for pdf in self.pdf_list:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    writer.add_page(page)

            with open(out_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Successo", "File PDF uniti con successo!")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore:\n{str(e)}")


if __name__ == "__main__":
    app = PdfManagerApp()
    app.mainloop()
