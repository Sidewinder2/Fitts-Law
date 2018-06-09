## Build Command

Run the following command to build a single executable file:

`pyinstaller --onefile Fitts.py && cp default.sqlite dist/`

The program should be portable for a USB thumb drive as long as both the `Fitts.exe` and `default.sqlite` files are copied from the `dist/` folder to the same destination folder.

[Source](https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263)
