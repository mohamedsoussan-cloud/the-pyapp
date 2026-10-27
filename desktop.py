"""Client Windows The Printing Yassine : fenêtre de bureau vers le serveur central."""
import json
import os
import sys
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog

import webview

APP_NAME = "The Printing Yassine Desktop"


def app_dir():
    return Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


def config_dir():
    root = os.environ.get("APPDATA") or str(Path.home())
    path = Path(root) / "The Printing Yassine"
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_url(value):
    value = (value or "").strip().rstrip("/")
    if not (value.startswith("https://") or value.startswith("http://127.0.0.1") or value.startswith("http://localhost")):
        raise ValueError("L'adresse doit commencer par https:// (ou localhost pour les tests).")
    return value


def read_config():
    for path in (app_dir() / "server_url.json", config_dir() / "server_url.json"):
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                value = validate_url(data.get("server_url", ""))
                return value
            except Exception:
                continue
    return ""


def ask_for_url():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        value = simpledialog.askstring(
            "Configuration initiale",
            "Entrez l'adresse HTTPS du serveur The Printing Yassine :\n\nExemple : https://the-printing-yassine.onrender.com",
            parent=root,
        )
        if not value:
            return ""
        value = validate_url(value)
        (config_dir() / "server_url.json").write_text(
            json.dumps({"server_url": value}, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return value
    except Exception as exc:
        messagebox.showerror("Adresse invalide", str(exc), parent=root)
        return ""
    finally:
        root.destroy()


def check_server(url):
    try:
        request = urllib.request.Request(url + "/api/health", headers={"User-Agent": "ThePrintingYassineDesktop/1.0"})
        with urllib.request.urlopen(request, timeout=12) as response:
            if response.status != 200:
                return False, f"Le serveur a répondu avec le code {response.status}."
            data = json.loads(response.read().decode("utf-8"))
            if not data.get("ok"):
                return False, "Le serveur répond mais sa base de données est indisponible."
            return True, ""
    except Exception as exc:
        return False, f"Impossible de joindre le serveur : {exc}"


def main():
    url = os.environ.get("PRINTING_YASSINE_SERVER_URL", "").strip() or read_config() or ask_for_url()
    if not url:
        return
    try:
        url = validate_url(url)
    except Exception as exc:
        root = tk.Tk(); root.withdraw(); messagebox.showerror("Configuration invalide", str(exc)); root.destroy(); return

    ok, reason = check_server(url)
    if not ok:
        root = tk.Tk(); root.withdraw()
        messagebox.showerror(
            "Serveur indisponible",
            reason + "\n\nVérifiez l'adresse et votre connexion Internet. L'adresse configurée peut être modifiée dans %APPDATA%\\The Printing Yassine\\server_url.json."
        )
        root.destroy()
        return

    webview.create_window(
        APP_NAME, url + "/login", width=1400, height=900,
        min_size=(1000, 650), resizable=True, confirm_close=True
    )
    webview.start()


if __name__ == "__main__":
    main()
