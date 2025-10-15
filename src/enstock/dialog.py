
import tkinter as tk
from tkinter import filedialog

def get_purchase_order():

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")],
    )

    if not pdf_path:
        print("No file selected. Exiting.")
        exit()

    # Read the selected PDF as bytes
    with open(pdf_path, "rb") as f:
        doc_data = f.read()

    return doc_data