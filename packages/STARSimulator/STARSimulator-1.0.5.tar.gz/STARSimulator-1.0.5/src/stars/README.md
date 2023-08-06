This program is a MIPS Assembly simulator made for the purpose of education.
## Dependencies
* PySide6 (v6.4 or newer)
* numpy (v1.23 or newer for Windows)
* opengl

# How to run:
Install the package.
```
$ pip install STARSimulator
```

Finally, run the program.
```
$ STARS [-h] [-a] [-d] [-g] [-n MAX_INSTRUCTIONS] [--noGui] [-i] [-w] [-pa PA [PA ...]] [filename]
```

# Positional arguments:
* `filename`       Input MIPS Assembly file.

# optional arguments:
* `-h`, `--help`     Shows help message and exits
* `-a`, `--assemble`    Assemble program without running it
* `-d`, `--debug`    Enables debugging mode
* `-g`, `--garbage`  Enables garbage data
* `-n`, `--max_instructions`  Sets max number of instructions
* `--noGui` no GUI, CLI only
* `-i`, `--disp_instr_count`  Displays the total instruction count
* `-w`, `--warnings`  Enables warnings
* `-pa`  Program arguments for the MIPS program


# Troubleshooting
* If you are on Mac (especially Big Sur) and the gui mainwindow doesn't lauch, run `export QT_MAC_WANTS_LAYER=1` in the terminal.
