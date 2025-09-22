import tkinter as tk
from tkinter import scrolledtext, Entry, Label
import os
import subprocess
import re
class TerminalEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("VFS Terminal Emulator")  # Имя VFS в заголовке
        # Текущая рабочая директория
        self.current_dir = os.getcwd()
        # Создаем виджеты
        self.create_widgets()
        # Приветственное сообщение
        self.output_text.insert(tk.END, f"VFS Terminal Emulator v1.0\nCurrent directory: {self.current_dir}\n$ ")
        self.output_text.see(tk.END)
    def create_widgets(self):
        # Область вывода
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=25, bg='black', fg='white')
        self.output_text.pack(padx=10, pady=10)
        self.output_text.config(state=tk.DISABLED)
        # Поле ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        Label(input_frame, text="$", fg='green', bg='black').pack(side=tk.LEFT)
        self.input_entry = Entry(input_frame, bg='black', fg='white', insertbackground='white')
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.bind("<Return>", self.process_command)
    def parse_arguments(self, command_line):
        """Парсит аргументы команды с раскрытием переменных окружения"""
        # Регулярное выражение для поиска переменных вида $VAR или ${VAR}
        env_var_pattern = r'\$(\w+)|(?<!\\)\$\{(\w+)\}'
        def replace_env_vars(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, f'${var_name}')
        # Заменяем переменные окружения
        processed_line = re.sub(env_var_pattern, replace_env_vars, command_line)
        # Разбиваем на аргументы (упрощенная версия)
        args = []
        current_arg = ""
        in_quotes = False
        escape_next = False
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
        """Обрабатывает введенную команду"""
        command_line = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        if not command_line:
            return
        # Парсим аргументы
        try:
            args = self.parse_arguments(command_line)
            if not args:
                return
            command = args[0]
            command_args = args[1:]
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"{command_line}\n")
            # Обработка команд
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
        # Добавляем приглашение для следующей команды
        self.output_text.insert(tk.END, f"$ ")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    def execute_ls(self, args):
        """Заглушка для команды ls"""
        self.output_text.insert(tk.END, f"ls command executed with arguments: {args}\n")
        self.output_text.insert(tk.END, f"Current directory: {self.current_dir}\n")
        # Имитация вывода файлов
        try:
            files = os.listdir(self.current_dir)
            for file in files[:5]:  # Показываем первые 5 файлов для демонстрации
                self.output_text.insert(tk.END, f"{file}\n")
            if len(files) > 5:
                self.output_text.insert(tk.END, "... (and more)\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error listing directory: {str(e)}\n")
    def execute_cd(self, args):
        """Заглушка для команды cd"""
        self.output_text.insert(tk.END, f"cd command executed with arguments: {args}\n")
        if not args:
            # cd без аргументов - переход в домашнюю директорию
            new_dir = os.environ.get('HOME', '/')
        else:
            new_dir = args[0]
        try:
            # Проверяем существование директории
            if os.path.isdir(new_dir):
                self.current_dir = os.path.abspath(new_dir)
                self.output_text.insert(tk.END, f"Changed directory to: {self.current_dir}\n")
            else:
                self.output_text.insert(tk.END, f"Error: Directory '{new_dir}' does not exist\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error changing directory: {str(e)}\n")
def main():
    root = tk.Tk()
    terminal = TerminalEmulator(root)
    root.mainloop()
if __name__ == "__main__":
    main()