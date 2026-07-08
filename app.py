import customtkinter as ctk
from utils import _

# Importiamo tutte le classi dei frame
from frames.home import HomeFrame
from frames.split import SplitFrame
from frames.merge import MergeFrame
from frames.protect import ProtectFrame
from frames.unlock import UnlockFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class PdfManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(_("app_title"))
        self.geometry("800x600")
        self.minsize(600, 500)

        self.iconbitmap("icon_white.ico")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.lbl_app_name = ctk.CTkLabel(
            self.top_bar, text=_("app_title"), font=ctk.CTkFont(weight="bold", size=14)
        )
        self.lbl_app_name.grid(row=0, column=0, padx=15, pady=5, sticky="w")

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
