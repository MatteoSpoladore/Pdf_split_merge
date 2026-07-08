import customtkinter as ctk
from utils import _


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

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
