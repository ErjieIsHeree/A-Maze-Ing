
PROGRAM := a_maze_ing.py
SRC := configuration.py visualizator.py config.txt
REQUIREMENTS := requirements.txt
MODULE := mazegen-1.0-py3-none-any.whl


all: run clean

init-venv:
	python3 -m venv .venv
	source .venv/bin/activate

install: $(REQUIREMENTS) $(MODULE)
	python3 -m pip install -r requirements.txt

run: $(PROGRAM) $(SRC)
	python3 $(PROGRAM)

clean:
	find . -name __pycache__ -exec rm -rf {} + 
	rm -rf .mypy_cache

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 .
	mypy . --strict
