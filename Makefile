ARG_BASE = $(shell basename --suffix=.reti $(ARG))
.PHONY: all test clean

all: read-all-color

install:
	ln -sr ./src/main.py /usr/local/bin/reti_interpreter

read: _read clean
_read:
	./src/main.py -c -t -a -o -r -p -b 8 -d 32 -D 20 -s 2 -E 8 -U 4 -S 0 -m ./run/code.reti

read-verbose: _read-verbose clean
_read-verbose:
	./src/main.py -c -t -a -o -r -p -b 8 -d 32 -D 20 -s 2 -E 8 -U 4 -S 0 -v -m ./run/code.reti

read-color: _read-color clean
_read-color:
	./src/main.py -c -t -a -o -r -p -b 8 -d 32 -D 20 -s 2 -E 8 -U 4 -S 0 -C -v -m ./run/code.reti

shell: _shell clean
_shell:
	./src/main.py

extract:
	./extract_input_and_except.sh

test: _test clean
test-extract: extract _test clean
_test:
	# start with 'make test-arg ARG=file_basename'
	# ARG2=-g if for debugging
	./run_tests.sh $(ARG_BASE) $(ARG2)

help:
	./src/main.py -h -C
	./src/main.py -h > ./doc/help-page.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

setup_pyinstaller_linux:
	python -m pip install --upgrade pip
	pip install tabulate
	pip install pyinstaller
	pip install staticx
	pip install patchelf-wrapper

setup_pyinstaller_wine:
	WINEPREFIX=~/Applications/Windows10 WINEARCH=win32 winecfg
	WINEPREFIX=~/Applications/Windows10 WINEARCH=win32 wine ~/Applications/Windows10/drive_c/Python10/python.exe -m pip install --upgrade pip
	WINEPREFIX=~/Applications/Windows10 WINEARCH=win32 wine ~/Applications/Windows10/drive_c/Python10/python.exe -m pip install tabulate
	WINEPREFIX=~/Applications/Windows10 WINEARCH=win32 wine ~/Applications/Windows10/drive_c/Python10/python.exe -m pip install pyinstaller

setup_pyinstaller_windows:
	python -m pip install --upgrade pip
	pip install tabulate
	pip install pyinstaller

create_bin_linux:
	pyinstaller ./src/main.py --onefile --hidden-import=tabulate,cmd2,colorama,bitstring --distpath=./dist
	staticx ./dist/main ./dist/pico_c_compiler_linux
	rm ./dist/main

create_bin_wine:
	WINEPREFIX=~/Applications/Windows10 WINEARCH=win32 wine ~/Applications/Windows10/drive_c/Python10/Scripts/pyinstaller.exe ~/Applications/Windows10/drive_c/users/areo/Documents/Studium/pico_c_compiler/src/main.py  --onefile --hidden-import=tabulate --distpath=~/Documents/Studium/pico_c_compiler/dist
	mv ~/Documents/Studium/pico_c_compiler/dist/pico_c_compiler.exe ~/Documents/Studium/pico_c_compiler/dist/pico_c_compiler_wine.exe

create_bin_windows:
	pyinstaller src\main.py --onefile --hidden-import=tabulate,cmd2,colorama,bitstring --distpath=dist
	staticx ./dist/main.exe ./dist/pico_c_compiler_windows.exe
	# entferne ./dist/main.exe

exec_bin_linux:
	./dist/pico_c_compiler_linux -S

exec_bin_wine:
	WINEPREFIX=~/Applications/Windows10 WINEARCH=win32 wine ~/Applications/Windows10/drive_c/users/areo/Documents/Studium/pico_c_compiler/dist/pico_c_compiler_wine.exe -S

exec_bin_windows:
	# go into dist folder in explorer and ctrl+l and type cmd and hit enter
	pico_c_compiler_windows.exe -S
