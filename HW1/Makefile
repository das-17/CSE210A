#Referenced 'https://datatofish.com/executable-pyinstaller/' , 'https://pyinstaller.readthedocs.io/en/stable/usage.html'

all:
	pip install pyinstaller
	pyinstaller --onefile --windowed arith.py
	mv dist/arith .
	rm -rf ./dist
	rm -rf ./build
	rm -rf arith.spec