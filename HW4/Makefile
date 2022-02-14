all:
	pip install pyinstaller
	pip install lark-parser
	pyinstaller --onefile --windowed while-ss.py
	mv dist/while-ss .
	rm -rf ./dist
	rm -rf ./build
	rm -rf while-ss.spec