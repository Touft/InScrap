import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import scrape_videos
import config
import os
import random
from rich.console import Console

class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("InScrap V1.0")
        self.geometry("600x500")
        
        self.console = Console()

        self.configure(bg='#2c2c2c')
        
        self.download_thread = None
        self.stop_event = threading.Event()
        self.konami_code = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]
        self.konami_index = 0
        self.multi_color_mode = False
        
        self.image_path = "BROKEN :/"
        self.loaded_image = None
        
        self.create_widgets()
        
        self.bind_all('<Key>', self.check_konami_code)
        
    def create_widgets(self):
        self.label_fg = '#ffffff'
        self.entry_bg = '#444444'
        self.entry_fg = '#ffffff'
        self.button_bg = '#555555'
        self.button_fg = '#ffffff'
        self.text_bg = '#333333'
        self.text_fg = '#ffffff'
        
        tk.Label(self, text="Username:", bg=self['bg'], fg=self.label_fg).pack(pady=5)
        self.username_entry = tk.Entry(self, bg=self.entry_bg, fg=self.entry_fg)
        self.username_entry.insert(0, config.IG_USERNAME)
        self.username_entry.pack(pady=5)
        
        tk.Label(self, text="Password:", bg=self['bg'], fg=self.label_fg).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", bg=self.entry_bg, fg=self.entry_fg)
        self.password_entry.insert(0, config.IG_PASSWORD)
        self.password_entry.pack(pady=5)
        
        tk.Label(self, text="Output Folder:", bg=self['bg'], fg=self.label_fg).pack(pady=5)
        self.output_folder_entry = tk.Entry(self, bg=self.entry_bg, fg=self.entry_fg)
        self.output_folder_entry.insert(0, getattr(config, "OUTPUT_FOLDER", ""))
        self.output_folder_entry.pack(pady=5)
        tk.Button(self, text="Search...", command=self.browse_folder, bg=self.button_bg, fg=self.button_fg).pack(pady=5)
        
        tk.Button(self, text="Save", command=self.save_settings, bg=self.button_bg, fg=self.button_fg).pack(pady=10)
        self.download_button = tk.Button(self, text="Start download", command=self.start_download, bg='#4CAF50', fg=self.button_fg)
        self.download_button.pack(pady=10)
        tk.Button(self, text="Stop download", command=self.stop_download, bg='#ff3333', fg=self.button_fg).pack(pady=10)
        
        self.output_text = tk.Text(self, height=10, width=60, bg=self.text_bg, fg=self.text_fg)
        self.output_text.pack(pady=5)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder)
    
    def save_config(self, username, password, output_folder):
        config_lines = []
        with open('config.py', 'r') as f:
            config_lines = f.readlines()

        with open('config.py', 'w') as f:
            for line in config_lines:
                if line.startswith("IG_USERNAME"):
                    f.write(f'IG_USERNAME = "{username}"\n')
                elif line.startswith("IG_PASSWORD"):
                    f.write(f'IG_PASSWORD = "{password}"\n')
                elif line.startswith("OUTPUT_FOLDER"):
                    f.write(f'OUTPUT_FOLDER = "{output_folder}"\n')
                else:
                    f.write(line)
            if not any(line.startswith("OUTPUT_FOLDER") for line in config_lines):
                f.write(f'OUTPUT_FOLDER = "{output_folder}"\n')
    
    def save_settings(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        output_folder = self.output_folder_entry.get()

        self.save_config(username, password, output_folder)
        self.update_output_text("Settings saved!\n", 'success')
    
    def start_download(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        output_folder = self.output_folder_entry.get()

        if not os.path.exists(output_folder):
            messagebox.showerror("Error", f"Unable to locate the folder: {output_folder}")
            return

        self.save_config(username, password, output_folder)

        self.stop_event.clear()
        self.download_thread = threading.Thread(target=self.run_bot, args=(username, password, output_folder), daemon=True)
        self.download_thread.start()
    
    def stop_download(self):
        if self.download_thread and self.download_thread.is_alive():
            self.stop_event.set()
            self.update_output_text("Stopping current download...\n", 'info')
            self.download_thread.join()
            self.update_output_text("The bot has been stopped.\n", 'error')
    
    def run_bot(self, username, password, output_folder):
        self.update_output_text("Starting download...\n", 'info')
        try:
            scrape_videos.scrapeVideos(username=username, password=password, output_folder=output_folder, days=1, stop_event=self.stop_event)
            if not self.stop_event.is_set():
                self.update_output_text("Download successfully completed.\n", 'success')
        except Exception as e:
            self.update_output_text(f"Error: {e}\n", 'error')
    
    def update_output_text(self, message, msg_type='info'):
        color_map = {
            'info': '#00bfff',
            'success': '#00ff00',
            'error': '#ff3333'
        }
        self.console.print(message, style=color_map.get(msg_type, '#ffffff'))
        self.output_text.insert(tk.END, message, ('colored',))
        self.output_text.tag_config('colored', foreground=color_map.get(msg_type, '#ffffff'))
        self.output_text.see(tk.END)
        self.update()

    def check_konami_code(self, event):
        keysym_to_keycode = {
            'Up': 38, 'Down': 40, 'Left': 37, 'Right': 39, 'b': 66, 'a': 65
        }
        key = event.keysym
        keycode = keysym_to_keycode.get(key, None)
        
        if keycode is not None and keycode == self.konami_code[self.konami_index]:
            self.konami_index += 1
            if self.konami_index == len(self.konami_code):
                self.activate_multi_color_mode()
                self.konami_index = 0
        else:
            self.konami_index = 0
    
    def activate_multi_color_mode(self):
        self.multi_color_mode = True
        self.update_output_text("Multicolor mode activated!\n", 'success')
        
        if self.loaded_image is None:
            self.loaded_image = Image.open(self.image_path)
            self.loaded_image = self.loaded_image.resize((400, 300), Image.ANTIALIAS)
            self.loaded_image = ImageTk.PhotoImage(self.loaded_image)
        
        self.image_label = tk.Label(self, image=self.loaded_image, bg=self['bg'])
        self.image_label.pack(pady=10)

if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
