import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import struct

class FileEncryptor:
    def __init__(self, key, padding_size=512):
        self.key = key
        self.padding_size = padding_size  # Size of padding to add after encryption

    def encrypt(self, inputFile, outputFile):
        try:
            with open(inputFile, 'rb') as fin, open(outputFile, 'wb') as fout:
                # Read and encrypt the original content
                content = fin.read()
                for byte in content:
                    fout.write(bytes([byte + self.key]))  # Simple encryption (add key)
                
                # Add padding to increase file size
                padding = bytes([random.randint(0, 255) for _ in range(self.padding_size)])  # Random padding
                fout.write(padding)  # Write padding at the end

                # Store padding size at the end of the file (last 4 bytes)
                fout.write(struct.pack("I", self.padding_size))

            # Hide the original file by renaming it
            hidden_file = inputFile + ".original"
            os.rename(inputFile, hidden_file)  # Renaming it as a backup with ".original"
            messagebox.showinfo("Success", f"File encrypted successfully to {outputFile}. Original file hidden.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt file: {str(e)}")

    def decrypt(self, inputFile, outputFile):
        try:
            with open(inputFile, 'rb') as fin, open(outputFile, 'wb') as fout:
                # Read the encrypted content
                content = fin.read()

                # Extract the padding size from the last 4 bytes of the file
                padding_size = struct.unpack("I", content[-4:])[0]  # Unpack the last 4 bytes to get the padding size

                # Remove the padding bytes
                content_without_padding = content[:-4 - padding_size]  # Remove padding + padding size info

                # Decrypt content by subtracting the key from each byte
                for byte in content_without_padding:
                    fout.write(bytes([byte - self.key]))  # Simple decryption (subtract key)

            messagebox.showinfo("Success", f"File decrypted successfully to {outputFile}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt file: {str(e)}")


class FileEncryptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor")
        self.file_encryptor = None

        # Create Widgets
        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.key_label = tk.Label(root, text="Enter Key:")
        self.key_label.pack(pady=5)

        self.key_entry = tk.Entry(root)
        self.key_entry.pack(pady=5)

        self.operation_var = tk.StringVar(value="Encrypt")
        self.encrypt_radio = tk.Radiobutton(root, text="Encrypt", variable=self.operation_var, value="Encrypt")
        self.decrypt_radio = tk.Radiobutton(root, text="Decrypt", variable=self.operation_var, value="Decrypt")
        self.encrypt_radio.pack(pady=5)
        self.decrypt_radio.pack(pady=5)

        self.start_button = tk.Button(root, text="Start", command=self.start_operation)
        self.start_button.pack(pady=20)

        self.file_path = None

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_label.config(text=os.path.basename(self.file_path))

    def start_operation(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file")
            return

        try:
            key = int(self.key_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer")
            return

        fe = FileEncryptor(key)

        if self.operation_var.get() == "Encrypt":
            output_file = self.file_path + ".enc"
            fe.encrypt(self.file_path, output_file)
        elif self.operation_var.get() == "Decrypt":
            if self.file_path.endswith(".enc"):
                output_file = self.file_path[:-4]  # Remove '.enc'
                fe.decrypt(self.file_path, output_file)
                # After decryption, you can optionally move the original hidden file back
                hidden_file = self.file_path + ".original"
                if os.path.exists(hidden_file):
                    os.rename(hidden_file, self.file_path)  # Restore original file
            else:
                messagebox.showerror("Error", "Selected file is not encrypted")

# Create the main window
root = tk.Tk()
app = FileEncryptorGUI(root)
root.geometry("300x300")  # Window size
root.mainloop()
