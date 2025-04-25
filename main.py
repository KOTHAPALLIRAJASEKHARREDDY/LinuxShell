import os
import subprocess
import glob
from colorama import Fore, Style, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory

# Color setup
init(autoreset=True)

# Completer class for tab suggestions
class SmartCompleter(Completer):
    def __init__(self):
        self.commands = ['cd', 'clear', 'exit', 'help', 'history', 'ls', 'cat', 'pwd', 'echo', 'mkdir', 'rmdir']

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        matches = [cmd for cmd in self.commands if cmd.startswith(word)]
        matches += glob.glob(word + '*')
        for m in matches:
            yield Completion(m, start_position=-len(word))

# Initialize completer and history
completer = SmartCompleter()
shell_history = InMemoryHistory()
command_history = []

# Welcome Banner
def welcome_banner():
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════╗
║          🐍  WELCOME TO MY SHELL           ║
║         Built with ❤️ in Python            ║
╚══════════════════════════════════════════╝
""")
    print(Fore.GREEN + "Type 'help' to see available commands!\n")

# Expand wildcards (like *.py)
def expand_wildcards(cmd_parts):
    expanded = []
    for part in cmd_parts:
        if '*' in part:
            expanded += glob.glob(part)
        else:
            expanded.append(part)
    return expanded

# Main shell loop
def run_shell():
    while True:
        try:
            command = prompt("myShell> ", completer=completer, history=shell_history).strip()
            if not command:
                continue

            command_history.append(command)

            # EXIT
            if command.lower() == "exit":
                # Save history on exit
                with open("history.txt", "w") as f:
                    for cmd in command_history:
                        f.write(cmd + "\n")
                print(Fore.YELLOW + "Command history saved to 'history.txt'")
                print(Fore.RED + "Bye Mowa! 👋")
                break

            # CD command
            if command.startswith("cd "):
                path = command[3:].strip()
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(Fore.RED + f"No such directory: {path}")
                continue

            # PWD command
            if command.strip() == "pwd":
                print(os.getcwd())
                continue

            # MKDIR command
            if command.startswith("mkdir "):
                folder = command[6:].strip()
                try:
                    os.mkdir(folder)
                    print(Fore.GREEN + f"Directory '{folder}' created!")
                except FileExistsError:
                    print(Fore.RED + f"Directory '{folder}' already exists.")
                continue

            # RMDIR command
            if command.startswith("rmdir "):
                folder = command[6:].strip()
                try:
                    os.rmdir(folder)
                    print(Fore.GREEN + f"Directory '{folder}' removed!")
                except FileNotFoundError:
                    print(Fore.RED + f"No such directory: {folder}")
                except OSError:
                    print(Fore.RED + f"Directory '{folder}' is not empty or cannot be removed.")
                continue

            # CLEAR screen
            if command.strip() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue

            # HELP
            if command.strip() == "help":
                print(Fore.YELLOW + """
myShell - Available Commands:

exit               : Exit the shell
cd [path]          : Change directory
pwd                : Print current working directory
ls                 : List files and folders
mkdir [name]       : Create a new directory
rmdir [name]       : Remove an empty directory
clear              : Clear the screen
help               : Show help menu
history            : Show previous commands
>                  : Redirect output to file
<                  : Read input from file
|                  : Pipe output to another command
&                  : Run command in background
""")
                continue

            # HISTORY
            if command.strip() == "history":
                for i, cmd in enumerate(command_history, 1):
                    print(f"{i}: {cmd}")
                continue

            # Handle 'ls' manually
            if command.strip() == "ls":
                files = os.listdir()
                for f in files:
                    print(f)
                continue

            # Handle 'echo' manually
            if command.startswith("echo "):
                print(command[5:].strip())
                continue

            # Background process (&)
            if command.endswith("&"):
                cmd = command[:-1].strip().split()
                cmd = expand_wildcards(cmd)
                subprocess.Popen(cmd)
                print(Fore.GREEN + f"Started background job: {' '.join(cmd)}")
                continue

            # Output redirection (>)
            if ">" in command:
                cmd_parts = command.split(">")
                cmd = cmd_parts[0].strip().split()
                cmd = expand_wildcards(cmd)
                outfile = cmd_parts[1].strip()
                with open(outfile, "w") as out:
                    subprocess.run(cmd, stdout=out)
                continue

            # Input redirection (<)
            if "<" in command:
                cmd_parts = command.split("<")
                cmd = cmd_parts[0].strip().split()
                cmd = expand_wildcards(cmd)
                infile = cmd_parts[1].strip()
                with open(infile, "r") as inp:
                    subprocess.run(cmd, stdin=inp)
                continue

            # PIPES
            if "|" in command:
                commands = [c.strip().split() for c in command.split("|")]
                commands = [expand_wildcards(c) for c in commands]
                p1 = subprocess.Popen(commands[0], stdout=subprocess.PIPE)
                p2 = subprocess.Popen(commands[1], stdin=p1.stdout)
                p1.stdout.close()
                p2.communicate()
                continue

            # Normal command run
            cmd_parts = command.split()
            cmd_parts = expand_wildcards(cmd_parts)
            subprocess.run(cmd_parts)

        except FileNotFoundError:
            print(Fore.RED + "Command not found 🤷‍♂️")
        except KeyboardInterrupt:
            print(Fore.RED + "\nUse 'exit' to quit!")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    welcome_banner()
    run_shell()
