import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import re
import time
import threading
import tkinter.font as tkfont

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Chatbot")
        self.root.geometry("400x500")
        self.dark_mode = True
        self.create_widgets()
        self.update_theme()

    def create_widgets(self):
        self.chat_window = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD, font=("Arial", 12))
        self.chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Define italic font for "typing" tag
        italic_font = tkfont.Font(self.chat_window, self.chat_window.cget("font"))
        italic_font.configure(slant="italic")
        self.chat_window.tag_configure("typing", foreground="#AAAAAA", font=italic_font)
        self.chat_window.tag_configure("user", foreground="cyan")
        self.chat_window.tag_configure("bot", foreground="lightgreen")

        self.input_box = tk.Entry(self.root, font=("Arial", 12))
        self.input_box.pack(pady=10, padx=10, fill=tk.X)
        self.input_box.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.toggle_button = tk.Button(self.root, text="Toggle Dark/Light Mode", command=self.toggle_theme)
        self.toggle_button.pack(pady=5)

    def update_theme(self):
        if self.dark_mode:
            self.root.config(bg="#2E2E2E")
            self.chat_window.config(bg="#3C3C3C", fg="white", insertbackground="white")
            self.input_box.config(bg="#3C3C3C", fg="white", insertbackground="white")
            self.send_button.config(bg="#4C4C4C", fg="white")
            self.toggle_button.config(bg="#4C4C4C", fg="white")
        else:
            self.root.config(bg="white")
            self.chat_window.config(bg="white", fg="black", insertbackground="black")
            self.input_box.config(bg="white", fg="black", insertbackground="black")
            self.send_button.config(bg="lightgray", fg="black")
            self.toggle_button.config(bg="lightgray", fg="black")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def send_message(self, event=None):
        user_input = self.input_box.get()
        if user_input.strip():
            self.display_message(user_input, "user")
            self.input_box.delete(0, tk.END)
            threading.Thread(target=self.bot_response, args=(user_input,)).start()

    def display_message(self, message, sender):
        self.chat_window.config(state='normal')
        if sender == "user":
            self.chat_window.insert(tk.END, f"You: {message}\n", "user")
        elif sender == "bot_typing":
            self.chat_window.insert(tk.END, f"{message}\n", "typing")
        else:
            self.chat_window.insert(tk.END, f"Bot: {message}\n", "bot")
        self.chat_window.yview(tk.END)
        self.chat_window.config(state='disabled')

    def bot_response(self, user_input):
        self.display_message("Bot is typing...", "bot_typing")
        time.sleep(1)  # Simulate thinking time
        self.chat_window.config(state='normal')
        # Remove the typing indicator line
        self.chat_window.delete('end-2l linestart', 'end-1c lineend')
        self.chat_window.config(state='disabled')

        response = self.get_response(user_input)
        self.display_message(response, "bot")

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        if re.match(r'^(hi|hello|hey)$', user_input):
            return "Hello! How can I assist you today?"
        elif "time" in user_input or "date" in user_input:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif re.match(r'^\d+(\.\d+)?\s*[\+\-\*/]\s*\d+(\.\d+)?$', user_input):
            try:
                return str(eval(user_input))
            except Exception:
                return "Error in calculation."
        else:
            return "I'm sorry, I don't understand that."

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
