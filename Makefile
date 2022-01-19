all:
	sudo pip install pyinstaller
	pyinstaller --onefile arith.py
	mv dist/arith .
	rm -fr dist/
	rm -fr build/
	find . -name '__pycache__' -exec rm -fr {} +
	rm arith.spec