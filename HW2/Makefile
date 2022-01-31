all:
	pip install pyinstaller
	pip install lark-parser
	pyinstaller --onefile --windowed while.py
	mv dist/while .
	rm -rf ./dist
	rm -rf ./build
	rm -rf while.spec