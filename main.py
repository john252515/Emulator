import tkinter as tk
from tkinter import scrolledtext
import os
import re
class TerminalEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("VFS Terminal Emulator")
        self.current_dir = os.getcwd()
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=25, bg='black', fg='white')
        self.output_text.pack(padx=10, pady=10)
        self.output_text.config(state=tk.DISABLED)
        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(input_frame, text="$", fg='green', bg='black').pack(side=tk.LEFT)
        self.input_entry = tk.Entry(input_frame, bg='black', fg='white', insertbackground='white')
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.bind("<Return>", self.process_command)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"VFS Terminal Emulator v1.0\nCurrent directory: {self.current_dir}\n$ ")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    def parse_arguments(self, command_line):
        env_var_pattern = r'\$(\w+)|(?<!\\)\$\{(\w+)\}'
        processed_line = re.sub(env_var_pattern,
                                lambda m: os.environ.get(m.group(1) or m.group(2), f'${m.group(1) or m.group(2)}'),
                                command_line)
        args, current_arg, in_quotes, escape_next = [], "", False, False
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
        command_line = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        if not command_line:
            return
        try:
            args = self.parse_arguments(command_line)
            if not args:
                return
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"{command_line}\n")
            command, command_args = args[0], args[1:]
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
        self.output_text.insert(tk.END, "$ ")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    def execute_ls(self, args):
        self.output_text.insert(tk.END,
                                f"ls command executed with arguments: {args}\nCurrent directory: {self.current_dir}\n")
        try:
            files = os.listdir(self.current_dir)
            for file in files[:5]:
                self.output_text.insert(tk.END, f"{file}\n")
            if len(files) > 5:
                self.output_text.insert(tk.END, "... (and more)\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error listing directory: {str(e)}\n")
    def execute_cd(self, args):
        self.output_text.insert(tk.END, f"cd command executed with arguments: {args}\n")
        new_dir = os.environ.get('HOME', '/') if not args else args[0]
        try:
            if os.path.isdir(new_dir):
                self.current_dir = os.path.abspath(new_dir)
                self.output_text.insert(tk.END, f"Changed directory to: {self.current_dir}\n")
            else:
                self.output_text.insert(tk.END, f"Error: Directory '{new_dir}' does not exist\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error changing directory: {str(e)}\n")
def main():
    root = tk.Tk()
    TerminalEmulator(root)
    root.mainloop()
if __name__ == "__main__":
    main()