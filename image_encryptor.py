import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np


class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("800x600")

        # Variables
        self.original_image = None
        self.processed_image = None
        self.image_path = None
        self.key = tk.StringVar(value="1234")  # Default key

        # Created A UI
        self.create_widgets()

    def create_widgets(self):
        # Frame for image display
        image_frame = tk.Frame(self.root)
        image_frame.pack(pady=10)

        # Original imageAS
        self.original_label = tk.Label(image_frame, text="Original Image", borderwidth=2, relief="groove")
        self.original_label.pack(side=tk.LEFT, padx=10)

        # Processed image
        self.processed_label = tk.Label(image_frame, text="Processed Image", borderwidth=2, relief="groove")
        self.processed_label.pack(side=tk.LEFT, padx=10)

        # Controls frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Load/Save buttons
        btn_load = tk.Button(control_frame, text="Load Image", command=self.load_image)
        btn_load.grid(row=0, column=0, padx=5)

        btn_save = tk.Button(control_frame, text="Save Image", command=self.save_image)
        btn_save.grid(row=0, column=1, padx=5)

        # Encryption methods
        method_frame = tk.LabelFrame(self.root, text="Encryption Methods")
        method_frame.pack(pady=10, padx=10, fill=tk.X)

        btn_swap = tk.Button(method_frame, text="Swap RGB", command=lambda: self.process_image("swap"))
        btn_swap.pack(side=tk.LEFT, padx=5)

        btn_xor = tk.Button(method_frame, text="XOR Encrypt", command=lambda: self.process_image("xor"))
        btn_xor.pack(side=tk.LEFT, padx=5)

        btn_invert = tk.Button(method_frame, text="Invert Pixels", command=lambda: self.process_image("invert"))
        btn_invert.pack(side=tk.LEFT, padx=5)

        # Key input
        key_frame = tk.Frame(self.root)
        key_frame.pack(pady=10)

        tk.Label(key_frame, text="Encryption Key:").pack(side=tk.LEFT)
        key_entry = tk.Entry(key_frame, textvariable=self.key)
        key_entry.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status = tk.StringVar()
        self.status.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            try:
                self.image_path = file_path
                self.original_image = Image.open(file_path)

                # Resize for display if too large
                if self.original_image.width > 350 or self.original_image.height > 350:
                    self.original_image.thumbnail((350, 350))

                self.display_image(self.original_image, self.original_label)
                self.processed_image = None
                self.display_image(None, self.processed_label)
                self.status.set(f"Loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG", "*.png"),
                                                                ("JPEG", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                try:
                    # Save with original quality
                    self.processed_image.save(file_path)
                    self.status.set(f"Saved: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("Warning", "No processed image to save")

    def process_image(self, method):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        try:
            img = self.original_image.copy()
            pixels = np.array(img)

            if method == "swap":
                # Swap RGB channels
                processed_pixels = pixels.copy()
                processed_pixels[:, :, 0] = pixels[:, :, 2]  # R <- B
                processed_pixels[:, :, 2] = pixels[:, :, 0]  # B <- R

            elif method == "xor":
                # XOR with key
                key = self.key.get()
                if not key:
                    messagebox.showwarning("Warning", "Please enter an encryption key")
                    return

                key_bytes = key.encode()
                key_length = len(key_bytes)
                processed_pixels = pixels.copy()

                for i in range(processed_pixels.shape[0]):
                    for j in range(processed_pixels.shape[1]):
                        for k in range(3):  # For each RGB channel
                            key_index = (i * processed_pixels.shape[1] + j + k) % key_length
                            processed_pixels[i, j, k] ^= key_bytes[key_index]

            elif method == "invert":
                # Invert pixel values
                processed_pixels = 255 - pixels

            else:
                return

            self.processed_image = Image.fromarray(processed_pixels)
            self.display_image(self.processed_image, self.processed_label)
            self.status.set(f"Image processed with {method} method")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")

    def display_image(self, image, label):
        if image:
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # Keep a reference
        else:
            label.config(image='')
            label.image = None


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
