import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import json
import os
import uuid
import regex as re


def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)


def save_person_info(person_info):
    filename = 'person_data.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    unique_id = str(uuid.uuid4())
    person_info['unique_id'] = unique_id
    data[unique_id] = person_info

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def validate_phone_number(phone_number):
    return re.fullmatch(r'^\d{10}$', phone_number)


def validate_email(email):
    return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)


def add_person():
    name = name_entry.get().strip()
    mother_name = mother_name_entry.get().strip()
    father_name = father_name_entry.get().strip()
    phone_number = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if not (name and phone_number):
        messagebox.showwarning("Warning", "Name and Phone Number are required fields.")
        return

    if not validate_phone_number(phone_number):
        messagebox.showwarning("Warning", "Invalid Phone Number. Please enter a 10-digit number.")
        return

    if email and not validate_email(email):
        messagebox.showwarning("Warning", "Invalid Email Address. Please enter a valid email.")
        return

    person_info = {
        'name': name,
        'mother_name': mother_name,
        'father_name': father_name,
        'phone_number': phone_number,
        'email': email,
        'address': address
    }

    save_person_info(person_info)
    generate_qr_code(json.dumps(person_info), f"{person_info['unique_id']}.png")
    messagebox.showinfo("Success", f"Person added successfully with Unique ID: {person_info['unique_id']}")


root = tk.Tk()
root.title("QR Code Generator")

# Custom title bar frame
title_bar = tk.Frame(root, bg="blue", relief=tk.SUNKEN, bd=2)
title_bar.pack(fill=tk.X)

# Title label inside the custom title bar
title_label = tk.Label(title_bar, text="QR Code Generator", fg="white", bg="blue", font=("Helvetica", 14, "bold"))
title_label.pack(pady=5)

# Main content area
content_frame = tk.Frame(root)
content_frame.pack(padx=20, pady=10)

tk.Label(content_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(content_frame, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(content_frame, text="Mother's Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
mother_name_entry = tk.Entry(content_frame, width=30)
mother_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(content_frame, text="Father's Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
father_name_entry = tk.Entry(content_frame, width=30)
father_name_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(content_frame, text="Phone Number:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(content_frame, width=30)
phone_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(content_frame, text="Email ID:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(content_frame, width=30)
email_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(content_frame, text="Address:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
address_entry = tk.Entry(content_frame, width=30)
address_entry.grid(row=5, column=1, padx=10, pady=5)

# Button with color
add_button = tk.Button(content_frame, text="Add Person", command=add_person, bg="green", fg="white")
add_button.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
