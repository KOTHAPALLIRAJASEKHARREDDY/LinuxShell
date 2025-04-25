import os
import subprocess
import glob
import time
import datetime
from colorama import Fore, Style, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory

# Color setup
init(autoreset=True)

# Track shell start time
start_time = time.time()

# Smart Completer
class SmartCompleter(Completer):
    def __init__(self):
        self.commands = [
            'cd', 'clear', 'exit', 'help', 'history', 'ls', 'ls -l', 'cat',
            'pwd', 'echo', 'mkdir', 'rmdir', 'touch', 'rm', 'whoami', 'date', 'uptime'
        ]

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

# Welcome banner
def welcome_banner():
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════╗
║          🐍  WELCOME TO MY SHELL           ║
║         Built with ❤️ in Python            ║
╚══════════════════════════════════════════╝
""")
    print(Fore.GREEN + "Type 'help' to see available commands!\n")

# Expand wildcards (*)
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
            path = os.getcwd()
            command = prompt(f"{path} $ ", completer=completer, history=shell_history).strip()
            if not command:
                continue

            command_history.append(command)

            # Exit
            if command.lower() == "exit":
                with open("history.txt", "w") as f:
                    for cmd in command_history:
                        f.write(cmd + "\n")
                print(Fore.YELLOW + "Command history saved to 'history.txt'")
                print(Fore.RED + "Bye Mawa! 👋")
                break

            # cd
            if command.startswith("cd "):
                path = command[3:].strip()
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(Fore.RED + f"No such directory: {path}")
                continue

            # pwd
            if command.strip() == "pwd":
                print(os.getcwd())
                continue

            # mkdir
            if command.startswith("mkdir "):
                folder = command[6:].strip()
                try:
                    os.mkdir(folder)
                    print(Fore.GREEN + f"Directory '{folder}' created!")
                except FileExistsError:
                    print(Fore.RED + f"Directory '{folder}' already exists.")
                continue

            # rmdir
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

            # touch
            if command.startswith("touch "):
                file_name = command[6:].strip()
                try:
                    open(file_name, 'a').close()
                    print(Fore.GREEN + f"File '{file_name}' created successfully!")
                except Exception as e:
                    print(Fore.RED + f"Error creating file: {e}")
                continue

            # rm
            if command.startswith("rm "):
                file_name = command[3:].strip()
                try:
                    os.remove(file_name)
                    print(Fore.GREEN + f"File '{file_name}' deleted successfully!")
                except FileNotFoundError:
                    print(Fore.RED + f"No such file: {file_name}")
                continue

            # clear
            if command.strip() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue

            # help
            if command.strip() == "help":
                print(Fore.YELLOW + """
myShell - Available Commands:

exit               : Exit the shell
cd [path]          : Change directory
pwd                : Print working directory
ls                 : List files
ls -l              : List files with size
mkdir [foldername] : Create new directory
rmdir [foldername] : Remove empty directory
touch [filename]   : Create new file
rm [filename]      : Remove a file
cat [filename]     : View file content
echo [message]     : Print a message
whoami             : Show current user
date               : Show current date and time
uptime             : Show how long shell running
history            : Show previous commands
clear              : Clear the screen
>                  : Redirect output
<                  : Redirect input
|                  : Pipe between commands
&                  : Run in background
""")
                continue

            # history
            if command.strip() == "history":
                for i, cmd in enumerate(command_history, 1):
                    print(f"{i}: {cmd}")
                continue

            # ls
            if command.strip() == "ls":
                files = os.listdir()
                for f in files:
                    print(f)
                continue

            # ls -l
            if command.strip() == "ls -l":
                files = os.listdir()
                for f in files:
                    size = os.path.getsize(f)
                    print(f"{f}\t{size} bytes")
                continue

            # echo
            if command.startswith("echo "):
                print(command[5:].strip())
                continue

            # cat
            if command.startswith("cat "):
                file_name = command[4:].strip()
                try:
                    with open(file_name, 'r') as f:
                        print(f.read())
                except FileNotFoundError:
                    print(Fore.RED + f"No such file: {file_name}")
                continue

            # whoami
            if command.strip() == "whoami":
                try:
                    print(os.getlogin())
                except:
                    print(Fore.RED + "Unable to get user name.")
                continue

            # date
            if command.strip() == "date":
                now = datetime.datetime.now()
                print(now.strftime("%Y-%m-%d %H:%M:%S"))
                continue

            # uptime
            if command.strip() == "uptime":
                seconds = int(time.time() - start_time)
                mins, secs = divmod(seconds, 60)
                print(f"Shell running for {mins} minutes {secs} seconds")
                continue

            # background &
            if command.endswith("&"):
                cmd = command[:-1].strip().split()
                cmd = expand_wildcards(cmd)
                subprocess.Popen(cmd)
                print(Fore.GREEN + f"Started background job: {' '.join(cmd)}")
                continue

            # redirection > and <
            if ">" in command:
                cmd_parts = command.split(">")
                cmd = cmd_parts[0].strip().split()
                cmd = expand_wildcards(cmd)
                outfile = cmd_parts[1].strip()
                with open(outfile, "w") as out:
                    subprocess.run(cmd, stdout=out)
                continue

            if "<" in command:
                cmd_parts = command.split("<")
                cmd = cmd_parts[0].strip().split()
                cmd = expand_wildcards(cmd)
                infile = cmd_parts[1].strip()
                with open(infile, "r") as inp:
                    subprocess.run(cmd, stdin=inp)
                continue

            # pipes
            if "|" in command:
                commands = [c.strip().split() for c in command.split("|")]
                commands = [expand_wildcards(c) for c in commands]
                p1 = subprocess.Popen(commands[0], stdout=subprocess.PIPE)
                p2 = subprocess.Popen(commands[1], stdin=p1.stdout)
                p1.stdout.close()
                p2.communicate()
                continue

            # normal commands
            cmd_parts = command.split()
            cmd_parts = expand_wildcards(cmd_parts)
            subprocess.run(cmd_parts)

        except FileNotFoundError:
            print(Fore.RED + f"Command not found: '{command.split()[0]}'. Type 'help' to see available commands.")
        except KeyboardInterrupt:
            print(Fore.RED + "\nUse 'exit' to quit!")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    welcome_banner()
    run_shell()
