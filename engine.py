import sys
import os
import threading
import subprocess
import socket
import customtkinter as ctk
from gpt4all import GPT4All

# Фикс путей для работы внутри EXE (PyInstaller)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AlphaEngine(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ALPHA AI ENGINE v1.1")
        self.geometry("750x850")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ПУТИ (ЗАМЕНИ ЕСЛИ ПЕРЕМЕСТИЛ МОДЕЛЬ)
        self.model_file = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
        self.model_path = r"C:\Users\user\Desktop\папки\Новая папка (8)"
        
        self.chat_history = []
        self.model = None

        self.setup_ui()
        
        # Загрузка ИИ в фоне, чтобы интерфейс не висел
        threading.Thread(target=self.load_model, daemon=True).start()

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, font=("Segoe UI", 15), wrap="word")
        self.textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.input_field = ctk.CTkEntry(self, placeholder_text="Введите приказ или вопрос...", font=("Segoe UI", 14))
        self.input_field.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        self.send_button = ctk.CTkButton(self, text="ОТПРАВИТЬ", command=self.send_message, state="disabled")
        self.send_button.grid(row=2, column=0, padx=20, pady=20)

        self.status_label = ctk.CTkLabel(self, text="СТАТУС: ЗАГРУЗКА ЯДРА...", text_color="yellow")
        self.status_label.grid(row=3, column=0, pady=5)

    def load_model(self):
        try:
            # Загрузка модели принудительно на CPU для стабильности в EXE
            self.model = GPT4All(
                model_name=self.model_file, 
                model_path=self.model_path, 
                allow_download=False,
                device='cpu'
            )
            self.append_text("Система: Ядро ИИ загружено. Все DLL подгружены.\n" + "-"*30 + "\n")
            self.send_button.configure(state="normal")
            self.status_label.configure(text="СТАТУС: ГОТОВ", text_color="green")
        except Exception as e:
            self.append_text(f"\n[ОШИБКА]: {e}")
            self.status_label.configure(text="СТАТУС: ОШИБКА", text_color="red")

    def append_text(self, text):
        self.textbox.insert("end", text)
        self.textbox.see("end")

    def send_message(self):
        txt = self.input_field.get()
        if txt and self.model:
            self.append_text(f"\nВы: {txt}\nАльфа: ")
            self.input_field.delete(0, "end")
            self.send_button.configure(state="disabled")
            threading.Thread(target=self.ai_logic, args=(txt,), daemon=True).start()

    def ai_logic(self, user_input):
        try:
            prompt = f"<|im_start|>system\nТы — Альфа, ИИ-движок.<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
            
            generator = self.model.generate(prompt, streaming=True, temp=0.3, max_tokens=300)
            
            for token in generator:
                if "<|im_end|>" in token: break
                self.append_text(token)
                self.update_idletasks()
            self.append_text("\n")
            
        except Exception as e:
            self.append_text(f"\n[ОШИБКА ГЕНЕРАЦИИ]: {e}")
        
        self.send_button.configure(state="normal")

    def on_closing(self):
        os._exit(0)

if __name__ == "__main__":
    app = AlphaEngine()
    app.mainloop()
