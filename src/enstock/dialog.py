
import tkinter as tk
from tkinter import filedialog
import os

def get_purchase_order():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    pdf_paths = filedialog.askopenfilenames(
        title="Select PDF file(s)",
        filetypes=[("PDF files", "*.pdf")],
    )

    if not pdf_paths:
        print("No file selected. Exiting.")
        exit()

    # Return list of tuples: (file_path, file_name, file_data)
    files = []
    for pdf_path in pdf_paths:
        file_name = os.path.basename(pdf_path)
        with open(pdf_path, "rb") as f:
            doc_data = f.read()
        files.append((pdf_path, file_name, doc_data))
    
    return files