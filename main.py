import subprocess
import os
import glob
from colorama import Fore, Style, init
init(autoreset=True)
if os.name == 'nt':
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter

else:
    import readline
    # 🔄 Tab autocomplete setup
    def complete(text, state):
        commands = ['cd', 'clear', 'exit', 'help', 'history']
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        matches += glob.glob(text + '*')
        try:
            return matches[state]
        except IndexError:
            return None


    # 🔧 Setup tab to trigger our completer
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")

command_history = []

def welcome_banner():
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════╗
║          🐍  WELCOME TO MY SHELL           ║
║         Built with ❤️ in Python            ║
╚══════════════════════════════════════════╝
""")
    print(Fore.GREEN + "Type 'help' to see available commands!\n")



def run_shell():
    while True:
        try:
            # Show prompt
            command = input("myShell> ").strip()

            # Exit command
            if command.lower() == "exit":
                print("Bye ! 👋")
                break

            # Ignore empty commands
            if not command:
                continue
            command_history.append(command)

            # Handle 'cd' manually
            if command.startswith("cd "):
                path = command[3:].strip()
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(f"No such directory: {path}")
                continue

            # Redirection handling
            if ">" in command:
                cmd_parts = command.split(">")
                cmd = cmd_parts[0].strip().split()
                outfile = cmd_parts[1].strip()
                with open(outfile, "w") as out:
                    subprocess.run(cmd, stdout=out)
                continue

            if "<" in command:
                cmd_parts = command.split("<")
                cmd = cmd_parts[0].strip().split()
                infile = cmd_parts[1].strip()
                with open(infile, "r") as inp:
                    subprocess.run(cmd, stdin=inp)
                continue

            # 🧪 Handle pipe |
            if "|" in command:
                commands = [c.strip().split() for c in command.split("|")]

                # First command
                p1 = subprocess.Popen(commands[0], stdout=subprocess.PIPE)

                # Second command takes input from first
                p2 = subprocess.Popen(commands[1], stdin=p1.stdout)

                # Close the stdout of p1 so it finishes properly
                p1.stdout.close()
                p2.communicate()
                continue

            # 🛠️ Handle background process with '&'
            if command.endswith("&"):
                cmd = command[:-1].strip().split()  # Remove '&' and split command
                subprocess.Popen(cmd)  # Run without waiting
                print(f"Started background job: {' '.join(cmd)}")
                continue

            # Built-in command: clear screen
            if command == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue

            # Built-in command: help
            if command == "help":
                print("""
            myShell - Available Commands:

            exit               : Exit the shell
            cd [path]          : Change directory
            clear              : Clear the screen
            help               : Show this help message
            &                  : Run command in background (e.g., sleep 5 &)
            >                  : Redirect output to file
            <                  : Read input from file
            |                  : Pipe output to another command
            """)
                continue

            if command == "history":
                for i, cmd in enumerate(command_history, 1):
                    print(f"{i}: {cmd}")
                continue

            # Run the command
            subprocess.run(command.split())

        except FileNotFoundError:
            print("Command not found 🤷‍♂️")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit!")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    welcome_banner()
    run_shell()
