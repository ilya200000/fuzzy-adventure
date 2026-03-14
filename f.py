import os, sys, subprocess, threading, json, socket
import customtkinter as ctk
from gpt4all import GPT4All

class AlphaEngine(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ALPHA AI ARMY ENGINE v1.0")
        self.geometry("800x600")
        
        # Путь к модели (теперь можно выбрать в меню)
        self.model_path = r"C:\Users\user\Desktop\папки\Новая папка (8)"
        self.model_file = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
        
        self.setup_ui()
        threading.Thread(target=self.load_ai, daemon=True).start()

    def setup_ui(self):
        self.log = ctk.CTkTextbox(self, width=760, height=400, font=("Consolas", 14))
        self.log.pack(pady=20, padx=20)
        
        self.cmd_input = ctk.CTkEntry(self, placeholder_text="Приказ Армии...", width=600, height=40)
        self.cmd_input.pack(pady=10)
        self.cmd_input.bind("<Return>", lambda e: self.process_order())

    def load_ai(self):
        try:
            self.model = GPT4All(model_name=self.model_file, model_path=self.model_path, device='cpu')
            self.log.insert("end", "[ENGINE] ИИ-Ядро запущено. Система готова.\n")
        except Exception as e:
            self.log.insert("end", f"[ERROR] Ошибка загрузки модели: {e}\n")

    def process_order(self):
        txt = self.cmd_input.get()
        self.cmd_input.delete(0, 'end')
        # Логика отправки команд ботам через сокеты или API
        self.log.insert("end", f"[YOU] {txt}\n")
        # Тут ИИ генерирует команду (come/kill/stop)
        res = self.model.generate(f"Command: {txt}\nAction:", max_tokens=5).strip().lower()
        self.log.insert("end", f"[AI] Сгенерирована тактика: {res.upper()}\n")

if __name__ == "__main__":
    AlphaEngine().mainloop()
