# maldev.py
import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Mapping of button keys to filenames and corresponding button attribute names
FILES = {
    "virus": {"filename": "virus.exe", "btn_attr": "virus_btn"},
    "ransomware": {"filename": "ransomware.exe", "btn_attr": "ransom_btn"},
    "rat": {"filename": "rat.exe", "btn_attr": "rat_btn"}
}

DECRYPTOR_SRC = "ransomware_decryptor.py"
RANSOMWARE_SRC = "ransomware_simulator.py"

class MalwareDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Malware Development Dashboard - Educational Use Only")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")
        self.setup_styles()
        self.create_widgets()
        self.ensure_required_files()
        self.check_files_exist()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#2b2b2b")
        style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("TButton",
                  background=[("active", "#404040"), ("pressed", "#505050")],
                  foreground=[("active", "#ffffff")])
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#4CAF50")
        style.configure("Warning.TLabel", font=("Segoe UI", 10), foreground="#ff6666")
        style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#aaaaaa")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="🔐 Malware Development Lab", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(main_frame, text="⚠️  FOR EDUCATIONAL USE ONLY - DO NOT DEPLOY  ⚠️",
                  style="Warning.TLabel").pack(pady=(0, 20))
        ttk.Label(main_frame, text="Export malware samples or build the ransomware simulator.",
                  justify=tk.CENTER).pack(pady=(0, 30))

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        self.virus_btn = ttk.Button(btn_frame, text="🦠 Export Virus",
                                    command=lambda: self.export_file("virus"), width=20)
        self.virus_btn.grid(row=0, column=0, padx=10, pady=10)

        self.ransom_btn = ttk.Button(btn_frame, text="🔒 Export Ransomware",
                                     command=lambda: self.export_file("ransomware"), width=20)
        self.ransom_btn.grid(row=0, column=1, padx=10, pady=10)

        self.rat_btn = ttk.Button(btn_frame, text="🐀 Export RAT",
                                  command=lambda: self.export_file("rat"), width=20)
        self.rat_btn.grid(row=0, column=2, padx=10, pady=10)

        build_frame = ttk.Frame(main_frame)
        build_frame.pack(pady=20)
        self.build_btn = ttk.Button(build_frame, text="⚙️ Build Ransomware & Decryptor EXEs",
                                    command=self.build_ransomware_exes, width=35)
        self.build_btn.pack()

        self.status_var = tk.StringVar(value="Ready.")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                               style="Status.TLabel", anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        ttk.Label(main_frame, text="This tool is for authorized cybersecurity training only.",
                  style="Status.TLabel").pack(side=tk.BOTTOM, pady=(5, 0))

    def ensure_required_files(self):
        """Create empty placeholder files if they don't exist."""
        for key, info in FILES.items():
            path = os.path.join(SCRIPT_DIR, info["filename"])
            if not os.path.isfile(path):
                with open(path, "wb") as f:
                    f.write(b"Placeholder for " + info["filename"].encode())
                print(f"[INFO] Created placeholder: {info['filename']}")

    def check_files_exist(self):
        """Update button states based on file presence."""
        missing = []
        for key, info in FILES.items():
            path = os.path.join(SCRIPT_DIR, info["filename"])
            btn = getattr(self, info["btn_attr"])
            if not os.path.isfile(path):
                missing.append(info["filename"])
                btn.state(["disabled"])
            else:
                btn.state(["!disabled"])
        if missing:
            self.status_var.set(f"⚠️ Missing: {', '.join(missing)}. Use 'Build Ransomware EXEs' or add files.")
        else:
            self.status_var.set("✅ All files present. Ready to export.")

    def export_file(self, file_type):
        info = FILES[file_type]
        src_filename = info["filename"]
        src_path = os.path.join(SCRIPT_DIR, src_filename)
        if not os.path.isfile(src_path):
            messagebox.showerror("File Not Found", f"Source '{src_filename}' missing.")
            return
        dest_path = filedialog.asksaveasfilename(
            title=f"Export {file_type.upper()} as...",
            initialfile=src_filename,
            defaultextension=".exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if not dest_path:
            return
        try:
            shutil.copy2(src_path, dest_path)
            messagebox.showinfo("Export Successful", f"Exported to:\n{dest_path}")
            self.status_var.set(f"Exported {src_filename} to {os.path.basename(dest_path)}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def build_ransomware_exes(self):
        """Compile the ransomware and decryptor Python scripts into EXEs using PyInstaller."""
        ransom_src = os.path.join(SCRIPT_DIR, RANSOMWARE_SRC)
        decrypt_src = os.path.join(SCRIPT_DIR, DECRYPTOR_SRC)
        missing = []
        if not os.path.isfile(ransom_src):
            missing.append(RANSOMWARE_SRC)
        if not os.path.isfile(decrypt_src):
            missing.append(DECRYPTOR_SRC)
        if missing:
            messagebox.showerror("Missing Source", f"Place these files in the script folder:\n{', '.join(missing)}")
            return

        if not messagebox.askyesno("Build EXEs",
                                   "This will compile the ransomware simulator and decryptor into EXE files.\n"
                                   "Requires PyInstaller to be installed.\nContinue?"):
            return

        self.status_var.set("Building ransomware.exe and decryptor.exe...")
        self.root.update()

        try:
            subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole",
                            "--name", "ransomware", ransom_src], check=True, cwd=SCRIPT_DIR)
            subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole",
                            "--name", "decryptor", decrypt_src], check=True, cwd=SCRIPT_DIR)

            dist_dir = os.path.join(SCRIPT_DIR, "dist")
            shutil.copy2(os.path.join(dist_dir, "ransomware.exe"), os.path.join(SCRIPT_DIR, "ransomware.exe"))
            shutil.copy2(os.path.join(dist_dir, "decryptor.exe"), os.path.join(SCRIPT_DIR, "decryptor.exe"))

            shutil.rmtree(os.path.join(SCRIPT_DIR, "build"), ignore_errors=True)
            shutil.rmtree(dist_dir, ignore_errors=True)
            for spec in ["ransomware.spec", "decryptor.spec"]:
                spec_path = os.path.join(SCRIPT_DIR, spec)
                if os.path.isfile(spec_path):
                    os.remove(spec_path)

            self.status_var.set("✅ Build successful! ransomware.exe and decryptor.exe created.")
            messagebox.showinfo("Build Complete", "ransomware.exe and decryptor.exe are ready.")
            self.check_files_exist()
        except subprocess.CalledProcessError as e:
            self.status_var.set("Build failed. Ensure PyInstaller is installed.")
            messagebox.showerror("Build Error", f"PyInstaller failed:\n{e}")
        except Exception as e:
            self.status_var.set("Build error.")
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = MalwareDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
