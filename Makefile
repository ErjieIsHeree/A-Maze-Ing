
# Las variables del Makefile

PROGRAM := main.py
SRC := 
MODULES := 
UNUSED_FILES := 

# Los recetas del Makefile

all:

install:
	python3 -m pip install $(MODULES)

run: $(PROGRAM) $(SRC)
	python3 $(PROGRAM)

debug:
	echo do debug

clean:
	rm -r $(UNUSED_FILES)

lint:
	python3 -m flake8
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
