
PROGRAM := a_maze_ing.py
SRC := configuration.py visualizator.py

REQUIREMENTS := requirements.txt
MODULE := mazegen-1.0-py3-none-any.whl

CONFIG := config.txt

install: $(REQUIREMENTS) $(MODULE) $(PIP)
	pip install -r $(REQUIREMENTS)

run: $(PROGRAM) $(SRC) $(CONFIG)
	python3 $(PROGRAM) $(CONFIG)

debug: $(PROGRAM) $(SRC) $(CONFIG)
	python3 -m pdb $(PROGRAM) $(CONFIG)

clean:
	find . -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict
