import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import tempfile
import requests
import os

# Optional: Add Tidy's path if not in system PATH
os.environ["PATH"] += os.pathsep + r"C:\Program Files\tidy 5.8.0\bin"

def analyze_code():
    lang = lang_choice.get()
    code = code_input.get("1.0", tk.END)

    with tempfile.NamedTemporaryFile(delete=False, suffix=get_extension(lang)) as temp_file:
        temp_file.write(code.encode())
        temp_path = temp_file.name

    if lang == "Python":
        result = subprocess.getoutput(f"pylint {temp_path}")
    elif lang == "C/C++":
        result = subprocess.getoutput(f"cppcheck --enable=all {temp_path}")
    elif lang == "Java":
        result = subprocess.getoutput(f"javac {temp_path}")
    elif lang == "JavaScript":
        result = subprocess.getoutput(f"eslint {temp_path}")
    elif lang == "HTML":
        # Use full path if needed
        tidy_path = r'"C:\Program Files\tidy 5.8.0\bin\tidy.exe"'
        result = subprocess.getoutput(f"{tidy_path} -errors -quiet {temp_path}")
    else:
        result = "Language not supported."

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

def fetch_website_html():
    url = website_url.get()
    try:
        response = requests.get(url)
        response.raise_for_status()
        code_input.delete("1.0", tk.END)
        code_input.insert(tk.END, response.text)
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error fetching website: {str(e)}")

def get_extension(lang):
    return {
        "Python": ".py",
        "C/C++": ".c",
        "Java": ".java",
        "JavaScript": ".js",
        "HTML": ".html"
    }.get(lang, ".txt")

# --- GUI Setup ---
window = tk.Tk()
window.title("Multi-Language Debugger Tool")
window.geometry("750x700")

tk.Label(window, text="Select Language:").pack()
lang_choice = ttk.Combobox(window, values=["Python", "C/C++", "Java", "JavaScript", "HTML"])
lang_choice.set("Python")
lang_choice.pack()

tk.Label(window, text="Enter Website URL (for HTML only):").pack(pady=(10, 0))
website_url = tk.Entry(window, width=60)
website_url.pack()
tk.Button(window, text="Fetch Website HTML", command=fetch_website_html).pack(pady=(2, 10))

code_input = scrolledtext.ScrolledText(window, width=90, height=15)
code_input.pack(pady=10)

tk.Button(window, text="Analyze Code", command=analyze_code).pack(pady=5)

output_box = scrolledtext.ScrolledText(window, width=90, height=15)
output_box.pack(pady=10)

window.mainloop()
