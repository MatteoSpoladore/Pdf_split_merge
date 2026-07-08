import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pypdf import PdfReader, PdfWriter
from utils import _


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
