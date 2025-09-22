import tkinter as tk
from tkinter import scrolledtext, Entry, Label
import os
import re
import sys
class TerminalEmulator:
    def __init__(self, root, vfs_path=None, script_path=None):
        self.root = root
        self.vfs_path = vfs_path
        self.script_path = script_path
        # Заголовок окна с именем VFS
        self.root.title(f"VFS Terminal Emulator - {self.vfs_path or 'default'}")
        # Рабочая директория (пока реальная ОС, позже заменим на VFS)
        self.current_dir = os.getcwd()
        # GUI
        self.create_widgets()
        # Отладочный вывод параметров
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"[DEBUG] VFS path = {self.vfs_path}\n")
        self.output_text.insert(tk.END, f"[DEBUG] Script path = {self.script_path}\n")
        self.output_text.config(state=tk.DISABLED)
        # Приветственное сообщение
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"VFS Terminal Emulator v1.1\nCurrent directory: {self.current_dir}\n$ ")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        # Если указан стартовый скрипт — запускаем
        if self.script_path:
            self.run_startup_script(self.script_path)
    def create_widgets(self):
        # Область вывода
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=25, bg='black', fg='white')
        self.output_text.pack(padx=10, pady=10)
        self.output_text.config(state=tk.DISABLED)
        # Поле ввода
        input_frame = tk.Frame(self.root, bg="black")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        Label(input_frame, text="$", fg='green', bg='black').pack(side=tk.LEFT)
        self.input_entry = Entry(input_frame, bg='black', fg='white', insertbackground='white')
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.bind("<Return>", self.process_command)
    def parse_arguments(self, command_line):
        """Парсер аргументов с раскрытием переменных окружения"""
        env_var_pattern = r'\$(\w+)|(?<!\\)\$\{(\w+)\}'
        def replace_env_vars(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, f'${var_name}')
        processed_line = re.sub(env_var_pattern, replace_env_vars, command_line)
        args, current_arg = [], ""
        in_quotes, escape_next = False, False
        for char in processed_line:
            if escape_next:
                current_arg += char
                escape_next = False
            elif char == '\\':
                escape_next = True
            elif char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ""
            else:
                current_arg += char
        if current_arg:
            args.append(current_arg)
        return args
    def process_command(self, event):
        """Обработка команд"""
        command_line = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        if not command_line:
            return
        try:
            args = self.parse_arguments(command_line)
            if not args:
                return
            command, command_args = args[0], args[1:]
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"{command_line}\n")
            if command == "exit":
                self.root.quit()
            elif command == "ls":
                self.execute_ls(command_args)
            elif command == "cd":
                self.execute_cd(command_args)
            else:
                self.output_text.insert(tk.END, f"Error: Unknown command '{command}'\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
        self.output_text.insert(tk.END, f"$ ")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    def execute_ls(self, args):
        self.output_text.insert(tk.END, f"ls executed with args: {args}\n")
        try:
            files = os.listdir(self.current_dir)
            for f in files[:10]:
                self.output_text.insert(tk.END, f"{f}\n")
            if len(files) > 10:
                self.output_text.insert(tk.END, "... (and more)\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
    def execute_cd(self, args):
        if not args:
            new_dir = os.environ.get("HOME", "C:\\")  # Windows fallback
        else:
            new_dir = args[0]
        # Если путь Unix-стиля на Windows
        if os.name == "nt" and new_dir.startswith("/"):
            new_dir = os.path.join("C:\\", new_dir.strip("/").replace("/", "\\"))
        try:
            if os.path.isdir(new_dir):
                self.current_dir = os.path.abspath(new_dir)
                self.output_text.insert(tk.END, f"Changed directory to: {self.current_dir}\n")
            else:
                self.output_text.insert(tk.END, f"Error: Directory '{new_dir}' does not exist\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
    def run_startup_script(self, path):
        """Выполнение стартового скрипта"""
        try:
            with open(path, "r") as f:
                for line in f:
                    cmd = line.strip()
                    if not cmd or cmd.startswith("#"):
                        continue
                    self.input_entry.insert(0, cmd)
                    self.process_command(None)
                    # Проверяем последние строки на наличие ошибки
                    last_lines = self.output_text.get("end-5l", "end-1l")
                    if "Error:" in last_lines:
                        self.output_text.insert(tk.END, f"Execution stopped due to error in script: {cmd}\n")
                        break
        except Exception as e:
            self.output_text.insert(tk.END, f"Error running script {path}: {str(e)}\n")
def main():
    vfs_path, script_path = None, None
    if len(sys.argv) > 1:
        vfs_path = sys.argv[1]
    if len(sys.argv) > 2:
        script_path = sys.argv[2]
    root = tk.Tk()
    terminal = TerminalEmulator(root, vfs_path, script_path)
    root.mainloop()
if __name__ == "__main__":
    main()