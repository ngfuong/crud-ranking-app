# Features
* Display list of films in scrollable list 
* Support sorting by score, alphabet, release date.
* Support CRUD and pop-up dialog to Edit/Add.

# Installation
Install packages
```
python -m venv .env
source .env/bin/activate 
pip install -r requirements.txt
```
Run application
```
source .env/bin/activate
python main.py
```

# Export to application
To export project to `.exe`, use `auto-py-to-exe`:
```
pip install auto-py-to-exe
auto-py-to-exe
```
Or run directly from terminal
```
pyinstaller --noconfirm --onefile --windowed  "main.py"
```
> **NOTE**: Put the .exe file in the same location as the resource folder.

