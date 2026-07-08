import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pypdf import PdfReader, PdfWriter
from utils import _


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
