import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import json
import os
import uuid
import regex as re  # Import regex module for validation


# Function to generate QR code
def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)


# Function to save person's information to JSON file
def save_person_info(person_info):
    filename = 'person_data.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    unique_id = str(uuid.uuid4())  # Generate a unique ID
    person_info['unique_id'] = unique_id
    data[unique_id] = person_info

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Function to validate phone number
def validate_phone_number(phone_number):
    # Regex for a valid phone number (10 digits)
    return re.fullmatch(r'^\d{10}$', phone_number)


# Function to validate email address
def validate_email(email):
    # Regex for a valid email address
    return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)


# Function to handle "Add Person" button click
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


# Main GUI window
root = tk.Tk()
root.title("QR Codifier")

# Labels and Entry Widgets
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Mother's Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
mother_name_entry = tk.Entry(root, width=30)
mother_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Father's Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
father_name_entry = tk.Entry(root, width=30)
father_name_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Phone Number:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Email ID:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Address:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
address_entry = tk.Entry(root, width=30)
address_entry.grid(row=5, column=1, padx=10, pady=5)

# Button to add person
add_button = tk.Button(root, text="Add Person", command=add_person)
add_button.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
