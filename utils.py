import locale


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
