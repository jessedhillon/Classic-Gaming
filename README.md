Classic Gaming for Boxee
========================

**v0.1**

This Boxee app provides a frontend to browse ROMs on your system and launch them using registered emulators. *This app is very rough right now, and has only been confirmed to work on Linux*, although it shouldn't be too hard to get it running on OSX or Windows. The app aims to recreate the Boxee App browser UI, for ROMs.

Usage
-----

1. Clone this repo into `~/.boxee/UserData/apps/com.devazero.classic_gaming/`
2. Create a MySQL database for storing configuration and ROM information.
3. Edit `connect` in `classic_gaming.py` so it has your database details.
4. Define an emulator with `cg_tool.py`, *e.g.*, this is how to define ZSNES:

    `$ cg_tool.py define snes 'Super NES' '/usr/bin/zsnes {rom_path}'`

5. Import ROMs into the system with:

    `$ cg_tool.py import snes /media/share/ROMs/snes/`

  * For best results, your ROM filename should be the name of the game. The script will attempt to identify ROMs by searching their filenames on GameFAQs.
6. Launch Boxee and run the app. The ROMs you imported should now be in there. Screenshots, descriptions and box covers will be grabbed from the GameFAQs website.

Roadmap
-------

1. Create a search sidebar.
2. Improve `cg_tool.py`.
3. Cross-platform compatibility.
4. Factor out configurable parameters into a config file.
5. Factor out {load, click} handlers into common functions.
6. Issue with OS X and fullscreen -- write an AppleScript to send keystroke for toggling fullscreen/windowed mode on Boxee.

Changelog
---------

*4/4/2011* 0.1, Initial release

About
-----

This app was created and is maintained by Jesse Dhillon. The current version of this app will always be found at [jesse0's GitHub](http://github.com/jesse0 "jesse0 on GitHub").
