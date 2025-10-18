import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import os
import uuid

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

# Global window reference for switching frames
root = tk.Tk()
root.title("UPI QR Generator")
root.geometry("900x700")


# ---------- SCREEN 1: Input Form ----------
def show_input_form():
    clear_window()

    tk.Label(root, text="Generate UPI Payment QR Code", font=("Arial", 20)).pack(pady=20)

    form_frame = tk.Frame(root)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Name:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
    name_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(form_frame, text="UPI ID:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    upi_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    upi_entry.grid(row=1, column=1)

    tk.Label(form_frame, text="Amount (INR):", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
    amount_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    amount_entry.grid(row=2, column=1)

    def on_submit():
        name = name_entry.get()
        upi_id = upi_entry.get()
        amount = amount_entry.get()

        if not name or not upi_id or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Generate transaction ID
        transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"

        # Generate UPI QR
        os.makedirs("static", exist_ok=True)

        # Generate UPI QR
        upi_string = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        qr = qrcode.make(upi_string)

        # Generate transaction ID
        transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"

# Save the QR code to static folder
        qr_path = f"D:\\upi\\static{transaction_id}.png"
        qr.save(qr_path)

# Show QR code screen
        show_qr_screen(transaction_id, qr_path)
        image = Image.open(qr_path)
        image = image.resize((500, 500), Image.Resampling.LANCZOS)  # Updated resizing constant
        gpay_img_ck = ImageTk.PhotoImage(image) 
        label = tk.Label(root, image=gpay_img_ck)
        label.image = gpay_img_ck  # Keep a reference to the image object
        label.pack(pady=10)
    tk.Button(root, text="Generate QR Code", font=("Arial", 14), command=on_submit).pack(pady=20)
    # GPay image
    try:
    # Correct variable name and resizing syntax
        gpay_image = Image.open(r"D:\upi\static\gpay.png")
        gpay_image = gpay_image.resize((800, 300), Image.Resampling.LANCZOS)  # Updated resizing constant
        gpay_img_tk = ImageTk.PhotoImage(gpay_image)

        img_label = tk.Label(root, image=gpay_img_tk)
        img_label.image = gpay_img_tk  # Keep a reference to the image object
        img_label.pack(pady=10)
    except Exception as e:
        tk.Label(root, text="Image not found: static/gpay.png", fg="red").pack()
        print(f"Error: {e}")


# ---------- SCREEN 2: QR Display ----------
def show_qr_screen(transaction_id, qr_path):
    clear_window()

    tk.Label(root, text="Scan & Pay via UPI", font=("Arial", 22)).pack(pady=20)
    tk.Label(root, text=f"Transaction ID: {transaction_id}", font=("Arial", 16)).pack(pady=10)

    try:
        img = Image.open(qr_path)
        img = img.resize((400, 400), Image.ANTIALIAS)
        qr_img = ImageTk.PhotoImage(img)
        img_label = tk.Label(root, image=qr_img)
        img_label.image = qr_img
        img_label.pack(pady=20)
    except:
        tk.Label(root, text="QR Code image not found!", fg="red", font=("Arial", 12)).pack()

    tk.Button(root, text="← Back", font=("Arial", 12), command=show_input_form).pack(pady=10)


# ---------- UTILITY ----------
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# ---------- Run App ----------
show_input_form()
root.mainloop()
