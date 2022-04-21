# Python-MunchkinLevelTracker

A simple python app to track the players scores while playing the card game Munchkin.
Uses pygame for everything GUI related.

This app is designed to be used on a ~16:9 touchscreen device, but can also be controlled via mouse and keyboard and supports any screen resolution.

## Features

* Track players score
* Highlights highest and lowest players
* Create, save and load games using the GUI
* Saved games are stored under `%APPDATA%\Munchkin` (Win), `~/.munchkin` (Linux) and `~/Library/Application Support/Munchkin` (Mac OS)

## How to use

The GUI launches on the screen, the mouse cursor is currently on.

After launching, start a new game and supply the players names. Confirm each name by pressing the return key.

To confirm the player selection, press enter a second time.

Use the keys <kbd>1</kbd> - <kbd>9</kbd> or tap the upper half of the screen to increase a players score.

To decrease it, tap the lower half or use <kbd>Shift</kbd>+<kbd>Number-Key</kbd>.

Use <kbd>Q</kbd> or the `Back`-Button to quit the game. The game is automatically saved after every action.

## How to use the code

* Clone or download this repository

* Install pygame using  
`pip install pygame`  
or  
`pip install -r requirements.txt`

* Execute `run.pyw` or start a run script suitable for your operating system or just run the munchkin folder as python module.

## Screenshots

_Coming soon_

## How to build

For bundeling the scripts as exe, the python library `pyinstaller` is required, which can be installed using the following command:

`pip install pyinstaller`

Run `pyinstaller run.spec` to build a single exe file inside a subdirectory called `dist`

## License

This app is distributed under GNU GPL version 3.0, which can be found in the file `LICENSE`.