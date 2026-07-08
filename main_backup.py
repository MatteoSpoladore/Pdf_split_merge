import os
import locale
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pypdf import PdfReader, PdfWriter


# --- IMPOSTAZIONI DI LOCALIZZAZIONE (i18n) ---
def get_system_language():
    try:
        sys_lang, _ = locale.getlocale()
        if sys_lang and sys_lang.lower().startswith("it"):
            return "it"
    except Exception:
        pass
    return "en"


CURRENT_LANG = get_system_language()

TRANSLATIONS = {
    "en": {
        "app_title": "PDF Manager: Split, Merge & Security",
        "btn_split_home": "SPLIT PDF",
        "btn_merge_home": "MERGE PDF",
        "btn_protect_home": "PROTECT PDF",
        "btn_unlock_home": "UNLOCK PDF",
        "btn_back": "< Back",
        "btn_select_file": "Select PDF File",
        "lbl_no_file": "No file selected",
        "btn_add_pdf": "Add PDF",
        "btn_remove_pdf": "Remove Selected",
        "btn_up": "Up ▲",
        "btn_down": "Down ▼",
        "msg_warn_title": "Warning",
        "msg_warn_no_file": "Please select a PDF file first.",
        "msg_warn_two_files": "Add at least two PDF files to merge.",
        "msg_err_title": "Error",
        "msg_err_generic": "An error occurred:\n",
        "msg_succ_title": "Success",
        "dialog_out_dir": "Select destination folder",
        "dialog_save_as": "Save PDF As",
        "btn_help": "?",
        "help_title": "User Guide",
        "help_text": "=== USER GUIDE ===\n\nSPLIT: Extract pages from a PDF.\nMERGE: Combine multiple PDFs.\nPROTECT: Add a password to a PDF.\nUNLOCK: Remove a password from a PDF (you must know the current password).",
        # Split
        "split_title": "Split PDF",
        "radio_single": "Extract every single page",
        "radio_range": "Extract by ranges (e.g., 2-3, 4-7)",
        "placeholder_range": "E.g., 1, 3, 5-8",
        "btn_exec_split": "Execute Split",
        "msg_err_range": "Invalid range format or pages out of bounds.",
        "msg_succ_split": "PDF split successfully!",
        # Merge
        "merge_title": "Merge PDF",
        "btn_exec_merge": "Confirm & Merge",
        "msg_succ_merge": "PDF files merged successfully!",
        # Protect & Unlock
        "protect_title": "Protect PDF with Password",
        "unlock_title": "Unlock PDF (Remove Password)",
        "lbl_password": "Enter Password:",
        "btn_exec_protect": "Apply Password & Save",
        "btn_exec_unlock": "Unlock & Save",
        "msg_succ_protect": "PDF protected successfully!",
        "msg_succ_unlock": "PDF unlocked successfully!",
        "msg_err_wrong_pass": "Incorrect password or file is not encrypted.",
    },
    "it": {
        "app_title": "PDF Manager: Separa, Unisci & Sicurezza",
        "btn_split_home": "SEPARA PDF",
        "btn_merge_home": "UNISCI PDF",
        "btn_protect_home": "PROTEGGI PDF",
        "btn_unlock_home": "SBLOCCA PDF",
        "btn_back": "< Indietro",
        "btn_select_file": "Seleziona File PDF",
        "lbl_no_file": "Nessun file selezionato",
        "btn_add_pdf": "Aggiungi PDF",
        "btn_remove_pdf": "Rimuovi Selezionato",
        "btn_up": "Su ▲",
        "btn_down": "Giù ▼",
        "msg_warn_title": "Attenzione",
        "msg_warn_no_file": "Seleziona prima un file PDF.",
        "msg_warn_two_files": "Aggiungi almeno due file PDF da unire.",
        "msg_err_title": "Errore",
        "msg_err_generic": "Si è verificato un errore:\n",
        "msg_succ_title": "Successo",
        "dialog_out_dir": "Seleziona cartella di destinazione",
        "dialog_save_as": "Salva PDF Come",
        "btn_help": "?",
        "help_title": "Guida all'Uso",
        "help_text": "=== GUIDA ALL'USO ===\n\nSEPARA: Estrai pagine da un documento.\nUNISCI: Combina più file in uno solo.\nPROTEGGI: Inserisci una password per bloccare il PDF.\nSBLOCCA: Rimuovi la password da un PDF (devi conoscere la password attuale).",
        # Split
        "split_title": "Separa PDF",
        "radio_single": "Estrai ogni singola pagina",
        "radio_range": "Estrai per intervalli (es. 2-3, 4-7)",
        "placeholder_range": "Es. 1, 3, 5-8",
        "btn_exec_split": "Esegui Separazione",
        "msg_err_range": "Formato intervalli non valido o pagine fuori range.",
        "msg_succ_split": "PDF separato con successo!",
        # Merge
        "merge_title": "Unisci PDF",
        "btn_exec_merge": "Conferma & Unisci",
        "msg_succ_merge": "File PDF uniti con successo!",
        # Protect & Unlock
        "protect_title": "Proteggi PDF con Password",
        "unlock_title": "Sblocca PDF (Rimuovi Password)",
        "lbl_password": "Inserisci Password:",
        "btn_exec_protect": "Applica Password & Salva",
        "btn_exec_unlock": "Sblocca & Salva",
        "msg_succ_protect": "PDF protetto con successo!",
        "msg_succ_unlock": "PDF sbloccato con successo!",
        "msg_err_wrong_pass": "Password errata o file non crittografato.",
    },
}


def _(key):
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["en"]).get(key, key)


# ---------------------------------------------

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class PdfManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(_("app_title"))
        self.geometry("800x600")
        self.minsize(600, 500)

        # Griglia principale dell'app
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- RIBBON BAR SUPERIORE ---
        self.top_bar = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.lbl_app_name = ctk.CTkLabel(
            self.top_bar, text=_("app_title"), font=ctk.CTkFont(weight="bold", size=14)
        )
        self.lbl_app_name.grid(row=0, column=0, padx=15, pady=5, sticky="w")

        # Pulsante Help (?)
        self.btn_help = ctk.CTkButton(
            self.top_bar,
            text=_("btn_help"),
            width=30,
            height=30,
            corner_radius=15,
            font=ctk.CTkFont(weight="bold", size=14),
            command=self.show_help,
        )
        self.btn_help.grid(row=0, column=1, padx=15, pady=5, sticky="e")

        # --- CONTENITORE DELLE SCHERMATE ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomeFrame, SplitFrame, MergeFrame, ProtectFrame, UnlockFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_help(self):
        help_window = ctk.CTkToplevel(self)
        help_window.title(_("help_title"))
        help_window.geometry("500x400")
        help_window.attributes("-topmost", True)
        help_window.resizable(False, False)

        textbox = ctk.CTkTextbox(
            help_window, width=460, height=360, wrap="word", font=ctk.CTkFont(size=14)
        )
        textbox.pack(padx=20, pady=20, fill="both", expand=True)
        textbox.insert("0.0", _("help_text"))
        textbox.configure(state="disabled")


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Griglia 2x2 per i pulsanti
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.btn_split = ctk.CTkButton(
            self,
            text=_("btn_split_home"),
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: controller.show_frame("SplitFrame"),
        )
        self.btn_split.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.btn_merge = ctk.CTkButton(
            self,
            text=_("btn_merge_home"),
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#2FA572",
            hover_color="#106A43",
            command=lambda: controller.show_frame("MergeFrame"),
        )
        self.btn_merge.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.btn_protect = ctk.CTkButton(
            self,
            text=_("btn_protect_home"),
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#C85000",
            hover_color="#8F3900",
            command=lambda: controller.show_frame("ProtectFrame"),
        )
        self.btn_protect.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.btn_unlock = ctk.CTkButton(
            self,
            text=_("btn_unlock_home"),
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#D13A3A",
            hover_color="#8F2525",
            command=lambda: controller.show_frame("UnlockFrame"),
        )
        self.btn_unlock.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)


class SplitFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.pdf_path = None

        self.btn_back = ctk.CTkButton(
            self,
            text=_("btn_back"),
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=(10, 20))

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
            fg_color="#C85000",
            hover_color="#8F3900",
            command=self.split_pdf,
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
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.btn_back = ctk.CTkButton(
            self,
            text=_("btn_back"),
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=(10, 20))

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

        self.btn_up = ctk.CTkButton(
            self.frame_order, text=_("btn_up"), width=60, command=self.move_up
        )
        self.btn_up.pack(pady=5)

        self.btn_down = ctk.CTkButton(
            self.frame_order, text=_("btn_down"), width=60, command=self.move_down
        )
        self.btn_down.pack(pady=5)

        self.btn_merge = ctk.CTkButton(
            self,
            text=_("btn_exec_merge"),
            command=self.merge_pdfs,
            fg_color="#2FA572",
            hover_color="#106A43",
        )
        self.btn_merge.pack(pady=20)

        self.pdf_list = []

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

        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx - 1, text)
        self.listbox.selection_set(idx - 1)
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

        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx + 1, text)
        self.listbox.selection_set(idx + 1)
        self.pdf_list[idx], self.pdf_list[idx + 1] = (
            self.pdf_list[idx + 1],
            self.pdf_list[idx],
        )

    def merge_pdfs(self):
        if len(self.pdf_list) < 2:
            messagebox.showwarning(_("msg_warn_title"), _("msg_warn_two_files"))
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title=_("dialog_save_as"),
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

            messagebox.showinfo(_("msg_succ_title"), _("msg_succ_merge"))
        except Exception as e:
            messagebox.showerror(_("msg_err_title"), _("msg_err_generic") + str(e))


class ProtectFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.pdf_path = None

        self.btn_back = ctk.CTkButton(
            self,
            text=_("btn_back"),
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=(10, 20))

        self.lbl_title = ctk.CTkLabel(
            self, text=_("protect_title"), font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_title.pack(pady=(0, 20))

        self.btn_select = ctk.CTkButton(
            self, text=_("btn_select_file"), command=self.select_pdf
        )
        self.btn_select.pack(pady=10)

        self.lbl_file = ctk.CTkLabel(self, text=_("lbl_no_file"))
        self.lbl_file.pack(pady=5)

        self.lbl_pass = ctk.CTkLabel(self, text=_("lbl_password"))
        self.lbl_pass.pack(pady=(20, 5))

        self.entry_password = ctk.CTkEntry(self, show="*", width=200)
        self.entry_password.pack(pady=5)

        self.btn_execute = ctk.CTkButton(
            self,
            text=_("btn_exec_protect"),
            fg_color="#C85000",
            hover_color="#8F3900",
            command=self.protect_pdf,
        )
        self.btn_execute.pack(pady=30)

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.pdf_path = path
            self.lbl_file.configure(text=os.path.basename(path))

    def protect_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning(_("msg_warn_title"), _("msg_warn_no_file"))
            return

        password = self.entry_password.get()
        if not password:
            messagebox.showwarning(_("msg_warn_title"), _("lbl_password"))
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title=_("dialog_save_as"),
        )
        if not out_path:
            return

        try:
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(password)

            with open(out_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo(_("msg_succ_title"), _("msg_succ_protect"))
            self.entry_password.delete(0, "end")
        except Exception as e:
            messagebox.showerror(_("msg_err_title"), _("msg_err_generic") + str(e))


class UnlockFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.pdf_path = None

        self.btn_back = ctk.CTkButton(
            self,
            text=_("btn_back"),
            width=100,
            command=lambda: controller.show_frame("HomeFrame"),
        )
        self.btn_back.pack(anchor="nw", padx=20, pady=(10, 20))

        self.lbl_title = ctk.CTkLabel(
            self, text=_("unlock_title"), font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_title.pack(pady=(0, 20))

        self.btn_select = ctk.CTkButton(
            self, text=_("btn_select_file"), command=self.select_pdf
        )
        self.btn_select.pack(pady=10)

        self.lbl_file = ctk.CTkLabel(self, text=_("lbl_no_file"))
        self.lbl_file.pack(pady=5)

        self.lbl_pass = ctk.CTkLabel(self, text=_("lbl_password"))
        self.lbl_pass.pack(pady=(20, 5))

        self.entry_password = ctk.CTkEntry(self, show="*", width=200)
        self.entry_password.pack(pady=5)

        self.btn_execute = ctk.CTkButton(
            self,
            text=_("btn_exec_unlock"),
            fg_color="#D13A3A",
            hover_color="#8F2525",
            command=self.unlock_pdf,
        )
        self.btn_execute.pack(pady=30)

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.pdf_path = path
            self.lbl_file.configure(text=os.path.basename(path))

    def unlock_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning(_("msg_warn_title"), _("msg_warn_no_file"))
            return

        password = self.entry_password.get()
        if not password:
            messagebox.showwarning(_("msg_warn_title"), _("lbl_password"))
            return

        try:
            reader = PdfReader(self.pdf_path)

            if reader.is_encrypted:
                success = reader.decrypt(password)
                if not success:
                    messagebox.showerror(_("msg_err_title"), _("msg_err_wrong_pass"))
                    return
            else:
                messagebox.showinfo(
                    _("msg_warn_title"), "Il file non è protetto da password."
                )
                return

            out_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                title=_("dialog_save_as"),
            )
            if not out_path:
                return

            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with open(out_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo(_("msg_succ_title"), _("msg_succ_unlock"))
            self.entry_password.delete(0, "end")
        except Exception as e:
            messagebox.showerror(_("msg_err_title"), _("msg_err_generic") + str(e))


if __name__ == "__main__":
    app = PdfManagerApp()
    app.mainloop()
