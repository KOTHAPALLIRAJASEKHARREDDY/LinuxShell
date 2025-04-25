# 🐍 Custom Python UNIX Shell

This project is a **custom UNIX Shell** built using **Python 3**.  
It mimics basic Unix-like command-line features and works **perfectly on Windows and Linux**.

---

## 🚀 Features

- Manual handling of basic commands:
  - `cd [path]`
  - `ls`
  - `ls -l`
  - `pwd`
  - `echo [message]`
  - `cat [filename]`
  - `touch [filename]`
  - `rm [filename]`
  - `mkdir [foldername]`
  - `rmdir [foldername]`
- Piping (`|`) support
- Input (`<`) and Output (`>`) Redirection
- Background job execution (`&`)
- Built-in Commands:
  - `clear`
  - `history`
  - `help`
  - `exit`
- **Tab Autocomplete** for commands and filenames
- **Arrow Key Support** (↑ ↓) for command history
- **Colorful Welcome Banner**
- **Session History Saved** into `history.txt` on exit

---

## ⚙️ How to Run

1. Install required libraries (once):

```bash
pip install prompt_toolkit colorama
```
 
2. Open cmd.exe or PowerShell (Important: don't run from PyCharm/VSCode console).


3. Navigate to your project folder:

```bash
cd path\to\your\project
```

4. Run the shell:

```bash
python main.py
```

## 🧪 Example Commands
- `myShell> whoami`
- `myShell> date`
- `myShell> uptime`
- `myShell> mkdir newfolder`
- `myShell> rmdir newfolder`
- `myShell> touch testfile.txt`
- `myShell> rm testfile.txt`
- `myShell> echo Hello World`
- `myShell> echo Hello > output.txt`
- `myShell> cat output.txt`
- `myShell> cat < input.txt`
- `myShell> ls`
- `myShell> ls -l`
- `myShell> ls | grep .py`
- `myShell> sleep 5 &`
- `myShell> history`
- `myShell> clear`
- `myShell> exit`


## ⚠️ Notes for Windows Users
- Run from `cmd.exe or PowerShell`, **NOT inside PyCharm or VSCode terminal**.


- Some Linux commands like ls, cat, pwd are manually handled inside Python.


- Full tab-autocomplete and arrow-key history supported via prompt_toolkit.



## 📖 Bonus Info
- On typing `exit`, all commands of the session are saved into history.txt.

- You can view previous session commands anytime!

## 🌟 Developed with ❤️ and Python

---

## 📜 License

© 2024 Rajasekhar Reddy Kothapalli. All rights reserved.

This project is developed as part of academic coursework for learning purposes.  
Unauthorized copying, distribution, or commercial usage is not allowed without prior permission.
