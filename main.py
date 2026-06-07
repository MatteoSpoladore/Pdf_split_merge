import os
import locale
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pypdf import PdfReader, PdfWriter


# --- IMPOSTAZIONI DI LOCALIZZAZIONE (i18n) ---
def get_system_language():
    try:
        # Tenta di leggere la lingua del sistema
        sys_lang, _ = locale.getlocale()
        if sys_lang and sys_lang.lower().startswith("it"):
            return "it"
    except Exception:
        pass
    return "en"  # Fallback all'inglese


CURRENT_LANG = get_system_language()

TRANSLATIONS = {
    "en": {
        "app_title": "PDF Manager: Split & Merge",
        "btn_split_home": "SPLIT PDF",
        "btn_merge_home": "MERGE PDF",
        "btn_back": "< Back",
        "split_title": "Split PDF",
        "btn_select_file": "Select PDF File",
        "lbl_no_file": "No file selected",
        "radio_single": "Extract every single page",
        "radio_range": "Extract by ranges (e.g., 2-3, 4-7)",
        "placeholder_range": "E.g., 1, 3, 5-8",
        "btn_exec_split": "Execute Split",
        "merge_title": "Merge PDF",
        "btn_add_pdf": "Add PDF",
        "btn_remove_pdf": "Remove Selected",
        "btn_up": "Up ▲",
        "btn_down": "Down ▼",
        "btn_exec_merge": "Confirm & Merge",
        "msg_warn_title": "Warning",
        "msg_warn_no_file": "Please select a PDF file first.",
        "msg_warn_two_files": "Add at least two PDF files to merge.",
        "msg_err_title": "Error",
        "msg_err_range": "Invalid range format or pages out of bounds.",
        "msg_err_generic": "An error occurred:\n",
        "msg_succ_title": "Success",
        "msg_succ_split": "PDF split successfully!",
        "msg_succ_merge": "PDF files merged successfully!",
        "dialog_out_dir": "Select destination folder",
        "dialog_save_as": "Save Merged PDF As",
    },
    "it": {
        "app_title": "PDF Manager: Separa & Unisci",
        "btn_split_home": "SEPARA PDF",
        "btn_merge_home": "UNISCI PDF",
        "btn_back": "< Indietro",
        "split_title": "Separa PDF",
        "btn_select_file": "Seleziona File PDF",
        "lbl_no_file": "Nessun file selezionato",
        "radio_single": "Estrai ogni singola pagina",
        "radio_range": "Estrai per intervalli (es. 2-3, 4-7)",
        "placeholder_range": "Es. 1, 3, 5-8",
        "btn_exec_split": "Esegui Separazione",
        "merge_title": "Unisci PDF",
        "btn_add_pdf": "Aggiungi PDF",
        "btn_remove_pdf": "Rimuovi Selezionato",
        "btn_up": "Su ▲",
        "btn_down": "Giù ▼",
        "btn_exec_merge": "Conferma & Unisci",
        "msg_warn_title": "Attenzione",
        "msg_warn_no_file": "Seleziona prima un file PDF.",
        "msg_warn_two_files": "Aggiungi almeno due file PDF da unire.",
        "msg_err_title": "Errore",
        "msg_err_range": "Formato intervalli non valido o pagine fuori range.",
        "msg_err_generic": "Si è verificato un errore:\n",
        "msg_succ_title": "Successo",
        "msg_succ_split": "PDF separato con successo!",
        "msg_succ_merge": "File PDF uniti con successo!",
        "dialog_out_dir": "Seleziona cartella di destinazione",
        "dialog_save_as": "Salva PDF Unito Come",
    },
}


def _(key):
    """Ritorna la traduzione associata alla chiave per la lingua corrente."""
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["en"]).get(key, key)


# ---------------------------------------------

# Impostazioni generali del tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class PdfManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(_("app_title"))
        self.geometry("800x600")
        self.minsize(600, 450)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomeFrame, SplitFrame, MergeFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sezione Sinistra
        self.frame_split = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_split.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_split.grid_rowconfigure(0, weight=1)
        self.frame_split.grid_columnconfigure(0, weight=1)

        self.btn_go_split = ctk.CTkButton(
            self.frame_split,
            text=_("btn_split_home"),
            font=ctk.CTkFont(size=24, weight="bold"),
            command=lambda: controller.show_frame("SplitFrame"),
        )
        self.btn_go_split.grid(row=0, column=0, sticky="nsew")

        # Sezione Destra
        self.frame_merge = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_merge.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.frame_merge.grid_rowconfigure(0, weight=1)
        self.frame_merge.grid_columnconfigure(0, weight=1)

        self.btn_go_merge = ctk.CTkButton(
            self.frame_merge,
            text=_("btn_merge_home"),
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

        self.btn_back = ctk.CTkButton(
            self,
            text=_("btn_back"),
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=20)

        self.lbl_title = ctk.CTkLabel(
            self, text=_("split_title"), font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_title.pack(pady=(0, 20))

        self.btn_select = ctk.CTkButton(
            self, text=_("btn_select_file"), command=self.select_pdf
        )
        self.btn_select.pack(pady=10)

        self.lbl_file = ctk.CTkLabel(self, text=_("lbl_no_file"))
        self.lbl_file.pack(pady=5)

        self.radio_var = tk.IntVar(value=0)

        self.radio_single = ctk.CTkRadioButton(
            self,
            text=_("radio_single"),
            variable=self.radio_var,
            value=0,
            command=self.toggle_entry,
        )
        self.radio_single.pack(pady=10)

        self.radio_range = ctk.CTkRadioButton(
            self,
            text=_("radio_range"),
            variable=self.radio_var,
            value=1,
            command=self.toggle_entry,
        )
        self.radio_range.pack(pady=10)

        self.entry_ranges = ctk.CTkEntry(
            self, placeholder_text=_("placeholder_range"), state="disabled", width=300
        )
        self.entry_ranges.pack(pady=5)

        self.btn_execute = ctk.CTkButton(
            self,
            text=_("btn_exec_split"),
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
            messagebox.showwarning(_("msg_warn_title"), _("msg_warn_no_file"))
            return

        out_dir = filedialog.askdirectory(title=_("dialog_out_dir"))
        if not out_dir:
            return

        try:
            reader = PdfReader(self.pdf_path)
            total_pages = len(reader.pages)
            base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]

            mode = self.radio_var.get()

            if mode == 0:
                for i in range(total_pages):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    out_path = os.path.join(out_dir, f"{base_name}_pag_{i+1}.pdf")
                    with open(out_path, "wb") as f:
                        writer.write(f)
            else:
                intervals_text = self.entry_ranges.get()
                chunks = self.parse_intervals(intervals_text, total_pages)

                if not chunks:
                    messagebox.showerror(_("msg_err_title"), _("msg_err_range"))
                    return

                for idx, chunk in enumerate(chunks):
                    writer = PdfWriter()
                    for p in chunk:
                        writer.add_page(reader.pages[p])

                    out_path = os.path.join(out_dir, f"{base_name}_part_{idx+1}.pdf")
                    with open(out_path, "wb") as f:
                        writer.write(f)

            messagebox.showinfo(_("msg_succ_title"), _("msg_succ_split"))
        except Exception as e:
            messagebox.showerror(_("msg_err_title"), _("msg_err_generic") + str(e))


class MergeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.btn_back = ctk.CTkButton(
            self,
            text=_("btn_back"),
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=20)

        self.lbl_title = ctk.CTkLabel(
            self, text=_("merge_title"), font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_title.pack(pady=(0, 10))

        self.frame_controls = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controls.pack(pady=10)

        self.btn_add = ctk.CTkButton(
            self.frame_controls, text=_("btn_add_pdf"), command=self.add_pdfs
        )
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_remove = ctk.CTkButton(
            self.frame_controls,
            text=_("btn_remove_pdf"),
            command=self.remove_pdf,
            fg_color="#D13A3A",
            hover_color="#8F2525",
        )
        self.btn_remove.grid(row=0, column=1, padx=5)

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

        self.frame_order = ctk.CTkFrame(self.listbox_frame, fg_color="transparent")
        self.frame_order.pack(side="right", fill="y", padx=10, pady=10)

        self
