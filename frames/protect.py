import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pypdf import PdfReader, PdfWriter
from utils import _


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

        # --- FRAME PER LA PASSWORD (ENTRY + PULSANTE) ---
        self.pass_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_frame.pack(pady=5)

        self.entry_password = ctk.CTkEntry(self.pass_frame, show="*", width=200)
        self.entry_password.pack(side="left", padx=(0, 5))

        self.btn_toggle_pass = ctk.CTkButton(
            self.pass_frame,
            text="👁",
            width=30,
            fg_color="#555555",
            hover_color="#333333",
            command=self.toggle_password_visibility,
        )
        self.btn_toggle_pass.pack(side="left")
        # ------------------------------------------------

        self.btn_execute = ctk.CTkButton(
            self,
            text=_("btn_exec_protect"),
            fg_color="#C85000",
            hover_color="#8F3900",
            command=self.protect_pdf,
        )
        self.btn_execute.pack(pady=30)

    def toggle_password_visibility(self):
        """Mostra o nasconde i caratteri della password e aggiorna l'icona."""
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
            self.btn_toggle_pass.configure(text="🔒")
        else:
            self.entry_password.configure(show="*")
            self.btn_toggle_pass.configure(text="👁")

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
            # Resetta la vista della password
            self.entry_password.configure(show="*")
            self.btn_toggle_pass.configure(text="👁")
        except Exception as e:
            messagebox.showerror(_("msg_err_title"), _("msg_err_generic") + str(e))

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

        # --- FRAME PER LA PASSWORD (ENTRY + PULSANTE) ---
        self.pass_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_frame.pack(pady=5)

        self.entry_password = ctk.CTkEntry(self.pass_frame, show="*", width=200)
        self.entry_password.pack(side="left", padx=(0, 5))

        self.btn_toggle_pass = ctk.CTkButton(
            self.pass_frame,
            text="👁",
            width=30,
            fg_color="#555555",
            hover_color="#333333",
            command=self.toggle_password_visibility,
        )
        self.btn_toggle_pass.pack(side="left")
        # ------------------------------------------------

        self.btn_execute = ctk.CTkButton(
            self,
            text=_("btn_exec_unlock"),
            fg_color="#D13A3A",
            hover_color="#8F2525",
            command=self.unlock_pdf,
        )
        self.btn_execute.pack(pady=30)

    def toggle_password_visibility(self):
        """Mostra o nasconde i caratteri della password e aggiorna l'icona."""
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
            self.btn_toggle_pass.configure(text="🔒")
        else:
            self.entry_password.configure(show="*")
            self.btn_toggle_pass.configure(text="👁")

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
            # Resetta la vista della password
            self.entry_password.configure(show="*")
            self.btn_toggle_pass.configure(text="👁")
        except Exception as e:
            messagebox.showerror(_("msg_err_title"), _("msg_err_generic") + str(e))
