import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import threading

# --- Professional Color Palette ---
BG_COLOR = "#ECEFF1"        # පසුබිම: ඉතා ලා අළු
HEADER_BG = "#2c3e50"       # උඩම තීරුව: තද නිල්
HERO_BG = "#1e3c72"         # AI කොටස: Tech Blue
CARD_BG = "#ffffff"         # මැද කොටස: සුදු
BTN_ACTION_BG = "#FF416C"   # ප්‍රධාන බට්න් එක: රෝස/රතු
BTN_BROWSE_BG = "#DFE6E9"   # Browse බට්න් එක: ලා අළු
TEXT_COLOR = "#2d3436"
TEXT_WHITE = "#ffffff"

# Fonts
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_FOOTER = ("Segoe UI", 9) # Footer එකට අලුත් ෆොන්ට් එකක්

# --- FFmpeg Setup Logic ---
def setup_ffmpeg():
    current_dir = os.getcwd()
    bin_path = os.path.join(current_dir, "bin")
    if os.path.exists(bin_path):
        os.environ["PATH"] += os.pathsep + bin_path
        return True
    return False

# --- Processing Logic ---
def separate_audio():
    song_path = file_path_var.get()
    
    if not song_path or song_path == "No file selected":
        messagebox.showerror("Selection Error", "Please select an MP3 file first!")
        return

    if not setup_ffmpeg():
        messagebox.showerror("System Error", "FFmpeg 'bin' folder not found!\nPlease ensure the setup is correct.")
        return

    process_btn.config(state=tk.DISABLED, text="Processing... ⏳")
    select_btn.config(state=tk.DISABLED)
    status_var.set("Running Demucs AI... Please wait (Approx. 1-2 mins)")
    status_label.config(foreground="#e67e22") 
    progress_bar.start(10)

    def run_process():
        try:
            command = f'demucs -n htdemucs --two-stems=vocals "{song_path}"'
            subprocess.run(command, shell=True, check=True, env=os.environ)
            root.after(0, lambda: on_success(song_path))
            
        except subprocess.CalledProcessError:
            root.after(0, on_error)

    threading.Thread(target=run_process, daemon=True).start()

def on_success(song_path):
    stop_processing()
    song_name = os.path.basename(song_path)
    messagebox.showinfo("Success", f"Separation Complete!\nCheck the 'separated' folder.")
    status_var.set(f"Successfully separated: {song_name} ✅")
    status_label.config(foreground="#27ae60")

def on_error():
    stop_processing()
    messagebox.showerror("Process Failed", "An error occurred during separation.\nCheck if FFmpeg files are in the 'bin' folder.")
    status_var.set("Error occurred during processing ❌")
    status_label.config(foreground="#c0392b")

def stop_processing():
    progress_bar.stop()
    process_btn.config(state=tk.NORMAL, text="Start Separation 🎵")
    select_btn.config(state=tk.NORMAL)

def select_file():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if filename:
        file_path_var.set(filename)
        status_var.set("Ready to process")
        status_label.config(foreground=TEXT_COLOR)

# --- GUI Setup ---
root = tk.Tk()
root.title("AI Audio Separator Pro")
root.geometry("750x600") # Footer එකට ඉඩ තියන්න උස ටිකක් වැඩි කළා
root.configure(bg=BG_COLOR)
root.resizable(True, True)

# Variables
file_path_var = tk.StringVar(value="No file selected")
status_var = tk.StringVar(value="Waiting for input...")

# 1. Top Bar (Header)
top_bar = tk.Frame(root, bg=HEADER_BG, height=50)
top_bar.pack(fill="x")
# Top bar එකේ තියෙන නම අයින් කරලා Footer එකට විතරක් දාන්න ඕන නම් මේ ලයින් එක මකන්න පුළුවන්, 
# නැත්නම් App Version එක විදියට තියන්න.
tk.Label(top_bar, text="AI Audio Tool V1.0", font=("Segoe UI", 9), bg=HEADER_BG, fg="#bdc3c7").pack(pady=10)

# 2. Main Wrapper
wrapper_frame = tk.Frame(root, bg=BG_COLOR)
wrapper_frame.pack(fill="both", expand=True, padx=30, pady=20)

# --- HERO SECTION (Blue Area) ---
hero_frame = tk.Frame(wrapper_frame, bg=HERO_BG, bd=0)
hero_frame.pack(fill="x", pady=(0, 0))

hero_inner = tk.Frame(hero_frame, bg=HERO_BG, padx=20, pady=30)
hero_inner.pack()

tk.Label(hero_inner, text="AI Audio Separator", font=FONT_TITLE, bg=HERO_BG, fg=TEXT_WHITE).pack()
tk.Label(hero_inner, text="Separate Vocals & Music using Deep Learning", font=FONT_SUBTITLE, bg=HERO_BG, fg="#a4b0be").pack(pady=(5, 0))

# --- WHITE CARD AREA ---
card_frame = tk.Frame(wrapper_frame, bg=CARD_BG, bd=1, relief="flat")
card_frame.pack(fill="both", expand=True, pady=(0, 10))

content_container = tk.Frame(card_frame, bg=CARD_BG)
content_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

# Step 1
tk.Label(content_container, text="STEP 1: Upload Song", font=FONT_BOLD, bg=CARD_BG, fg="#636e72").pack(anchor="w", pady=(10, 5))

input_frame = tk.Frame(content_container, bg=CARD_BG)
input_frame.pack(fill="x", pady=5)

file_entry = tk.Entry(input_frame, textvariable=file_path_var, font=FONT_NORMAL, state="readonly", bd=1, relief="solid", bg="#f1f2f6")
file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=5)

select_btn = tk.Button(input_frame, text="📂 Browse", command=select_file, font=FONT_NORMAL, bg=BTN_BROWSE_BG, fg=TEXT_COLOR, relief="flat", padx=15, pady=2)
select_btn.pack(side="right")

# Divider
ttk.Separator(content_container, orient='horizontal').pack(fill='x', pady=25)

# Step 2
tk.Label(content_container, text="STEP 2: Process Audio", font=FONT_BOLD, bg=CARD_BG, fg="#636e72").pack(anchor="w", pady=(0, 10))

process_btn = tk.Button(content_container, text="Start Separation 🎵", command=separate_audio, 
                        font=("Segoe UI", 12, "bold"), bg=BTN_ACTION_BG, fg="white", 
                        activebackground="#e03e5f", activeforeground="white", 
                        relief="flat", cursor="hand2", padx=30, pady=10)
process_btn.pack(pady=10)

style = ttk.Style()
style.theme_use('clam')
style.configure("Horizontal.TProgressbar", foreground=HERO_BG, background=HERO_BG)

progress_bar = ttk.Progressbar(content_container, orient="horizontal", length=400, mode="indeterminate", style="Horizontal.TProgressbar")
progress_bar.pack(pady=15)

status_label = tk.Label(content_container, textvariable=status_var, font=FONT_NORMAL, bg=CARD_BG, fg="#7f8c8d")
status_label.pack(pady=5)

# --- FOOTER SECTION (ඔයාගේ නම මෙතන) ---
footer_frame = tk.Frame(root, bg=BG_COLOR)
footer_frame.pack(side="bottom", fill="x", pady=10)

tk.Label(footer_frame, text="Designed & Developed by Sahan Tharuka", font=FONT_FOOTER, bg=BG_COLOR, fg="#7f8c8d").pack()
tk.Label(footer_frame, text="© 2025 All Rights Reserved", font=("Segoe UI", 8), bg=BG_COLOR, fg="#b2bec3").pack()

# Start App
root.mainloop()